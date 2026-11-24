# Input and output files
DESIGN_FILE = "design.csv"
COUNT_DIRECTORY = "counts_transcripts"
OUTPUT_FILE = "csv/transcript_counts.csv"

# Read sample names in the order listed in the design file
design = read.csv(DESIGN_FILE, stringsAsFactors = FALSE)

if (!"sample" %in% names(design)) {
  stop("The design file must contain a 'sample' column.")
}

if (anyDuplicated(design$sample)) {
  stop("Sample names in the design file must be unique.")
}

# Find each sample's featureCounts file
count_files = file.path(COUNT_DIRECTORY, paste0(design$sample, ".txt"))
missing_files = count_files[!file.exists(count_files)]

if (length(missing_files) > 0) {
  stop("Missing count file(s): ", paste(missing_files, collapse = ", "))
}

# Read transcript IDs and counts from one featureCounts file
read_sample_counts = function(count_file) {
  counts = read.delim(
    count_file,
    comment.char = "#",
    check.names = FALSE,
    stringsAsFactors = FALSE
  )

  if (!"Geneid" %in% names(counts) || ncol(counts) < 7L) {
    stop("Unexpected featureCounts format in: ", count_file)
  }

  transcript_counts = counts[[ncol(counts)]]

  if (!is.numeric(transcript_counts)) {
    transcript_counts = suppressWarnings(as.numeric(transcript_counts))
  }

  if (anyNA(transcript_counts)) {
    stop("Invalid count values in: ", count_file)
  }

  if (anyDuplicated(counts$Geneid)) {
    stop("Duplicate transcript IDs in: ", count_file)
  }

  data.frame(
    transcript_id = counts$Geneid,
    count = transcript_counts
  )
}

# Load each sample's counts
sample_counts = lapply(count_files, read_sample_counts)

# Collect all transcript IDs found in the files
transcript_ids = unique(unlist(
  lapply(sample_counts, function(counts) counts$transcript_id),
  use.names = FALSE
))

# Create a matrix with one column per sample
count_matrix = matrix(
  0,
  nrow = length(transcript_ids),
  ncol = nrow(design),
  dimnames = list(NULL, design$sample)
)

# Place each sample's counts in the matching transcript rows
for (sample_number in seq_along(sample_counts)) {
  counts = sample_counts[[sample_number]]
  transcript_rows = match(counts$transcript_id, transcript_ids)

  count_matrix[transcript_rows, sample_number] = counts$count
}

# Add transcript IDs to the count matrix
transcript_count_table = data.frame(
  transcript_id = transcript_ids,
  as.data.frame(count_matrix, check.names = FALSE),
  check.names = FALSE
)

# Save the combined matrix
dir.create(dirname(OUTPUT_FILE), recursive = TRUE, showWarnings = FALSE)
write.csv(transcript_count_table, OUTPUT_FILE, row.names = FALSE)