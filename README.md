# Original Language Study Bible

A mobile-friendly HTML study Bible prototype.

- English/NASB layer on top
- Hebrew or Greek original language on bottom
- Tap/click a word in either half to highlight linked words in both halves
- Supports importing aligned JSON files

## Copyright note

The full NASB text is copyrighted and is not bundled in this public prototype. To use NASB, import a licensed aligned JSON file using the same schema as the demo data in `index.html`.

## Run locally

```powershell
cd D:\OC\studyBible
python -m http.server 8770
```

Then open `http://localhost:8770/`.
