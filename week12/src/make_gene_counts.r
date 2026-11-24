
# Input and output files
INPUT_FILE = "csv/transcript_counts.csv"
OUTPUT_FILE = "csv/gene_counts_from_transcript_counts.csv"

# Read transcript count matrix
transcript_counts = read.csv(
  INPUT_FILE,
  stringsAsFactors = FALSE,
  check.names = FALSE
)

# Check required columns
if (!all(c("transcript_id", "gene_name") %in% names(transcript_counts))) {
  stop("Input file must contain transcript_id and gene_name columns.")
}

# Identify sample columns
sample_columns = setdiff(
  names(transcript_counts),
  c("transcript_id", "gene_name")
)

# Check for missing gene names
if (anyNA(transcript_counts$gene_name) ||
    any(transcript_counts$gene_name == "")) {
  stop("Missing gene names detected. Resolve annotations before collapsing.")
}

# Sum transcript counts belonging to the same gene
gene_counts = aggregate(
  transcript_counts[, sample_columns, drop = FALSE],
  by = list(gene_name = transcript_counts$gene_name),
  FUN = sum
)

# Save consolidated gene count matrix
dir.create(
  dirname(OUTPUT_FILE),
  recursive = TRUE,
  showWarnings = FALSE
)

write.csv(
  gene_counts,
  OUTPUT_FILE,
  row.names = FALSE
)

# Report results
cat("Transcript-level rows:", nrow(transcript_counts), "\n")
cat("Consolidated gene-level rows:", nrow(gene_counts), "\n")
cat("Genes consolidated:", nrow(transcript_counts) - nrow(gene_counts), "\n")
cat("Output saved to:", OUTPUT_FILE, "\n")
