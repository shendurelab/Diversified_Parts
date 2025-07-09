#!/usr/bin/env python

import sys
import re
import pandas as pd

def parse_cigar_for_read_coords(cigar_str):
    """
    Parse a (simplified) CIGAR string to find where alignment occurs on the read.
    Returns (read_start, read_end).
    
    We interpret:
      - S/H as soft/hard clips: advances the read pointer without using reference
      - M as alignment-consuming in both read & ref
      - We ignore complexities of I, D, N, etc. for brevity.
    """
    pattern = re.compile(r'(\d+)([MIDNSHP=X])')
    tokens = pattern.findall(cigar_str)
    
    read_pos = 0
    alignment_start = None
    aligned_length = 0
    
    for length_str, op in tokens:
        length = int(length_str)
        
        if op in ('S','H'):
            # If alignment hasn't started yet, these are leading clips
            # If alignment has started, these could be trailing clips
            # We just move read_pos but do not consume the reference
            read_pos += length
        
        elif op == 'M':
            # M consumes read bases (and reference bases)
            if alignment_start is None:
                alignment_start = read_pos
            read_pos += length
            aligned_length += length
        
        # If your data can have 'I', 'D', etc., handle them here:
        # e.g. 'I' -> read_pos += length, but does not consume reference
        # 'D' -> does not advance read_pos, but reference_pos += length
        # For a full solution, you'd parse them carefully.
    
    if alignment_start is None:
        return (None, None)
    
    alignment_end = alignment_start + aligned_length
    return (alignment_start, alignment_end)

def parse_sa_tag(sam_line):
    """
    Extract and parse the SA:Z supplementary alignments from the SAM line.
    Returns a list of dicts with keys: RNAME, CIGAR, POS, STRAND, MAPQ, NM.
    """
    match = re.search(r'SA:Z:([^\t]+)', sam_line)
    if not match:
        return []
    
    sa_value = match.group(1).rstrip(';')
    # SA:Z: has format: RNAME,POS,STRAND,CIGAR,MAPQ,NM;
    sa_entries = sa_value.split(';')
    
    results = []
    for entry in sa_entries:
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split(',')
        if len(parts) < 6:
            continue
        rname = parts[0]
        pos = int(parts[1])
        strand = parts[2]
        cigar = parts[3]
        mapq = int(parts[4])
        nm = int(parts[5])
        
        results.append({
            "RNAME": rname,
            "POS": pos,
            "STRAND": strand,
            "CIGAR": cigar,
            "MAPQ": mapq,
            "NM": nm
        })
    return results

def parse_sam_line(sam_line):
    """
    Parse a single SAM alignment line to get the primary alignment info and any SA:Z entries.
    Returns a list of dicts, each with:
       - Read_ID
       - VA_name (reference name)
       - Read_Start
       - Read_End
    """
    if sam_line.startswith('@'):
        # This is a header line; skip
        return []
    
    fields = sam_line.strip().split('\t')
    if len(fields) < 11:
        # Not a valid SAM alignment line
        return []
    
    qname = fields[0]
    flag = int(fields[1])
    rname = fields[2]
    # pos = int(fields[3])  # reference pos, not needed for read-based coords
    mapq = int(fields[4])
    cigar = fields[5]
    
    # 1) Primary alignment
    p_start, p_end = parse_cigar_for_read_coords(cigar)
    records = []
    
    if p_start is not None and p_end is not None:
        records.append({
            "Read_ID": qname,
            "VA_name": rname,
            "Read_Start": p_start,
            "Read_End": p_end
        })
    
    # 2) Check for SA:Z (supplementary alignments)
    sa_list = parse_sa_tag(sam_line)
    for sa in sa_list:
        s_start, s_end = parse_cigar_for_read_coords(sa["CIGAR"])
        if s_start is not None and s_end is not None:
            records.append({
                "Read_ID": qname,
                "VA_name": sa["RNAME"],
                "Read_Start": s_start,
                "Read_End": s_end
            })
    
    return records

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Parse a SAM file to produce a DataFrame of (Read_ID, VA_name, Read_Start, Read_End) sorted by read start."
    )
    parser.add_argument("--sam", required=True, help="Path to input SAM file")
    parser.add_argument("--out", default="va_parsed.csv", help="Output CSV file")
    args = parser.parse_args()
    
    all_records = []
    
    with open(args.sam, "r") as f:
        for line in f:
            recs = parse_sam_line(line)
            all_records.extend(recs)
    
    # Build DataFrame
    df = pd.DataFrame(all_records, columns=["Read_ID","VA_name","Read_Start","Read_End"])
    
    # Group by read, then sort by Read_Start
    # We can do a multi-step approach or just sort globally:
    df.sort_values(by=["Read_ID","Read_Start"], inplace=True)
    
    # Show a snippet
    print(df.head(20))
    print(f"Parsed {len(df)} alignments from {args.sam}.")
    
    # Write to CSV
    df.to_csv(args.out, index=False)
    print(f"Saved DataFrame to {args.out}")

if __name__ == "__main__":
    main()
