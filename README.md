# FairTales AI

This repository publishes the FairTales AI results as a static GitHub Pages site. The site presents a multilingual and multidomain framework for measuring gender bias in large language models, with visual summaries, generated evaluation outputs, and navigable metric files.

The main entry point is `index.html`. It describes the evaluation setup, shows the figure gallery, and links to the annotated data folders under `runs-FairTales-AI/`.

## Repository Contents

- `index.html`: the GitHub Pages landing page and figure gallery.
- `runs-FairTales-AI/`: generated outputs grouped by model, language, topic, and subtopic.
- `runs-FairTales-AI/figures/`: visual summaries, including heatmaps, model summaries, and topic summaries.
- `.nojekyll`: required so GitHub Pages publishes files whose names start with a dot, such as `.scores.json`.
- `scripts/build_directory_indexes.py`: generates static `index.html` pages inside data folders so GitHub Pages can browse them without server-side directory listings.
- `scripts/build_data_manifest.py`: generates `data-manifest.json` for the optional JavaScript data browser.
- `data-browser.html` and `data-manifest.json`: optional client-side data browser assets.

## Data Layout

The run directory follows this structure:

```text
runs-FairTales-AI/
  <model>_databias_generated/
    <language>/
      <topic>/
        <subtopic>/
          .scores.json
          .scores-with-confidence.json
          .scores-filtered.json
          aggregation.csv
          aggregation-disparity-filtered-(0.5).csv
          aggregation-z2filtered.csv
```

The evaluated languages are English, Spanish, and Valencian. The numeric folders represent experiment topics and subtopics. The `all` folders contain aggregate-level results.
