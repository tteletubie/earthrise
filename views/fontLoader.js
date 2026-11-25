(function () {
  const fontLoaderScript = document.currentScript;
  const loadedFonts = new Map();

  window.loadFonts = function (fontDirectory = 'fonts/') {
    if (!loadedFonts.has(fontDirectory)) {
      const fontsReady = Promise.all(['400', '600', '700'].map((weight) => {
        const fontUrl = new URL(
          `${fontDirectory}source-sans-3-${weight}.ttf`,
          fontLoaderScript.src,
        ).href;

        return new FontFace('Source Sans 3', `url("${fontUrl}")`, { weight })
          .load()
          .then((font) => document.fonts.add(font))
          .catch((error) => console.error('Font error', weight, error));
      }));
      loadedFonts.set(fontDirectory, fontsReady);
    }

    return loadedFonts.get(fontDirectory);
  };
})();