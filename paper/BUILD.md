# Building the paper

Toolchain: any standard TeX Live / MiKTeX distribution (the shipped PDF was
built with MiKTeX pdfTeX). No BibTeX run is needed (the bibliography is
inline), but labels and the table of cross-references require multiple
passes.

From this directory, run **three** pdflatex passes (a cold start needs
three for all cross-references to settle):

```
pdflatex -interaction=nonstopmode c2_equivariant_spherical_realizers_for_pythagorean_vertex_counts.tex
pdflatex -interaction=nonstopmode c2_equivariant_spherical_realizers_for_pythagorean_vertex_counts.tex
pdflatex -interaction=nonstopmode c2_equivariant_spherical_realizers_for_pythagorean_vertex_counts.tex
```

Expected: 10 pages, no errors, no undefined references.

Note: PDFs are not byte-reproducible across runs (embedded creation
timestamp and document ID); verify content, not bytes. Checksums of the
shipped artifacts are in `SHA256SUMS.txt`.
