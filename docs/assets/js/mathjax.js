window.MathJax = {
  loader: {
    load: ['[tex]/color', '[tex]/ams', 'output/svg'],
    failed: function (error) {                   // function to call if a component fails to load
      console.log(`MathJax(${error.package || '?'}): ${error.message}`);
    },
  },

  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\\[', '\\\]']],
    processEscapes: true,
    processEnvironments: true,
    packages: { '[+]': ['color'] },
    macros: {
      eqdef: "\\triangleq",
      red: ["{\\color{red}{#1}}", 1],
      green: ["{\\color{green}{#1}}", 1],
      blue: ["{\\color{blue}{#1}}", 1],
      cyan: ["{\\color{cyan}{#1}}", 1],
      magenta: ["{\\color{magenta}{#1}}", 1],
      yellow: ["{\\color{yellow}{#1}}", 1],
      black: ["{\\color{black}{#1}}", 1],
      gray: ["{\\color{gray}{#1}}", 1],
      white: ["{\\color{white}{#1}}", 1],
      darkgray: ["{\\color{darkgray}{#1}}", 1],
      lightgray: ["{\\color{lightgray}{#1}}", 1],
      brown: ["{\\color{brown}{#1}}", 1],
      lime: ["{\\color{lime}{#1}}", 1],
      olive: ["{\\color{olive}{#1}}", 1],
      orange: ["{\\color{orange}{#1}}", 1],
      pink: ["{\\color{pink}{#1}}", 1],
      purple: ["{\\color{purple}{#1}}", 1],
      teal: ["{\\color{teal}{#1}}", 1],
      violet: ["{\\color{violet}{#1}}", 1],
      p: ["{\\left( #1 \\right)}", 1],
      cb: ["{\\left\\{ #1 \\right\\}}", 1],
      sqb: ["{\\left[ #1 \\right]}", 1],
      abs: ["{\\left| #1 \\right|}", 1],
      an: ["{\\left\\langle #1 \\right\\rangle}", 1],
      ceil: ["{\\left\\lceil #1 \\right\\rceil}", 1],
      bb: ["{\\left\\llbracket #1 \\right\\rrbracket}", 1],
      tb: ["{\\textbf{#1}}", 1],
      ti: ["{\\emph{#1}}", 1],
      tallpipe: ["{\\begin{array}{r|l} #1 & #2 \\end{array}}", 2],
      join: "\\sqcup",
      meet: "\\sqcap",
      addsunion: "\\uplus",
      addsintersection: "\\mathrel{\\raisebox{.1em}{\\reflectbox{\\rotatebox[origin=c]{180}{\\addsunion}}}}",
      //
      Learner: "\\mathbb{L}",
      clg: "\\textrm{CLG}",
      lgraph: "\\mathcal{G}",
      edge: ["{{#1}\\!-\\!{#2}}", 2],
      reality: "\\textrm{REALITY}",
      reallysafe: "\\mathcal{S}",
      reallylive: "\\mathcal{L}",
      entangled: ["\\textrm{Entangled}\\left(#1, #2\\right)", 2],
      live: ["\\textrm{Live}\\left(#1\\right)", 1],
      correct: ["\\textrm{Correct}\\left(#1\\right)", 1],
      accurate: ["\\textrm{Accurate}\\left(#1\\right)", 1],
      terminating: ["\\textrm{Terminating}\\left(#1\\right)", 1],
      Safe: ["\\textrm{Safe}_{#1}", 1],
      Acc: ["\\textrm{Acc}_{#1}({#2})", 2],
      Value: "\\mathcal{V}",
      Message: "\\textrm{Message}",
      onea: "\\textrm{1a}",
      oneb: "\\textrm{1b}",
      twoa: "\\textrm{2a}",
      refs: "\\textrm{refs}",
      prev: "\\textrm{prev}",
      tran: ["\\textrm{Tran}\\left(#1\\right)", 1],
      prevtran: ["\\textrm{PrevTran}\\left({#1}\\right)", 1],
      sig: ["\\textrm{Sig}\\left(#1\\right)", 1],
      geta: ["\\textrm{Get1a}\\left({#1}\\right)", 1],
      ba: ["\\textrm{B}\\left(#1\\right)", 1],
      ChainRef: "\\textrm{ChainRef}",
      caughtEvidence: ["\\textrm{CaughtEvidence}({#1})", 1],
      caught: ["\\textrm{Caught}({#1})", 1],
      con: ["\\textrm{Con}_{{#1}}({#2})", 2],
      qa: ["\\textrm{q}\\left(#1\\right)", 1],
      fresh: ["\\textrm{fresh}_{#1}\\left(#2\\right)", 2],
      burying: ["\\textrm{burying}(#1, #2)", 2],
      buried: ["\\textrm{Buried}_{#1}(#2, #3)", 3],
      cona: ["\\textrm{Con2as}_{#1}\\left(#2\\right)", 2],
      iffound: ["\\textrm{IfFound}\\left(#1,#2\\right)", 2],
      vbr: ["\\textrm{R}_{#1}\\left(#2, #3\\right)", 3],
      va: ["\\textrm{V}\\left(#1\\right)", 1],
      vb: ["\\textrm{V}_{#1}\\left(#2\\right)", 2],
      vartype: ["{#1}:{#2}", 2],
      Decision: ["\\textrm{Decision}_{#1}\\left(#2\\right)", 2],
      wellformed: ["\\textrm{WellFormed}({#1})", 1],
      WellFormedOneB: ["\\textrm{WellFormed1B}({#1})", 1],
      WellFormedTwoA: ["\\textrm{WellFormed2A}({#1})", 1],
      argmax: "\\operatorname*{argmax}",
      andlinesTwo: ["\\begin{array}{r l} & {#1} \\\\ \\land & {#2} \\end{array}", 2],
      andlinesThree: ["\\begin{array}{r l} & {#1} \\\\ \\land & {#2} \\\\ \\land & {#3} \\end{array}", 3],
      andlinesFour: ["\\begin{array}{r l} & {#1} \\\\ \\land & {#2} \\\\ \\land & {#3} \\\\ \\land & {#4} \\end{array}", 4],
      andlinesFive: ["\\begin{array}{r l} & {#1} \\\\ \\land & {#2} \\\\ \\land & {#3} \\\\ \\land & {#4} \\\\ \\land & {#5} \\end{array}", 5],
      andlinesSix: ["\\begin{array}{r l} & {#1} \\\\ \\land & {#2} \\\\ \\land & {#3} \\\\ \\land & {#4} \\\\ \\land & {#5} \\\\ \\land & {#6} \\end{array}", 6],
      orlinesTwo: ["\\begin{array}{r l} & {#1} \\\\ \\lor & {#2} \\end{array}", 2],
      orlinesThree: ["\\begin{array}{r l} & {#1} \\\\ \\lor & {#2} \\\\ \\lor & {#3} \\end{array}", 3],
      orlinesFour: ["\\begin{array}{r l} & {#1} \\\\ \\lor & {#2} \\\\ \\lor & {#3} \\\\ \\lor & {#4} \\end{array}", 4],
      orlinesFive: ["\\begin{array}{r l} & {#1} \\\\ \\lor & {#2} \\\\ \\lor & {#3} \\\\ \\lor & {#4} \\\\ \\lor & {#5} \\end{array}", 5],
      hetdifftext: ["\\colorbox{LightBlue}{#1}", 1],
      // hetdiff: ["\\hetdifftext{$\\displaystyle#1$}", 1]
      hetdiff: ["{#1}", 1]
    }
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },

  chtml: {
    scale: 1,                      // global scaling factor for all expressions
    minScale: .5,                  // smallest scaling factor to use
    mtextInheritFont: false,       // true to make mtext elements use surrounding font
    merrorInheritFont: false,      // true to make merror text use surrounding font
    mtextFont: 'Roboto',                 // font to use for mtext, if not inheriting (empty means use MathJax fonts)
    merrorFont: 'serif',           // font to use for merror, if not inheriting (empty means use MathJax fonts)
    unknownFamily: 'serif',        // font to use for character that aren't in MathJax's fonts
    mathmlSpacing: false,          // true for MathML spacing rules, false for TeX rules
    skipAttributes: {},            // RFDa and other attributes NOT to copy to the output
    exFactor: .5,                  // default size of ex in em units
    displayAlign: 'center',        // default for indentalign when set to 'auto'
    displayIndent: '0'             // default for indentshift when set to 'auto'
  },

  svg: {
    scale: 1,                      // global scaling factor for all expressions
    minScale: .5,                  // smallest scaling factor to use
    mtextInheritFont: true,       // true to make mtext elements use surrounding font
    merrorInheritFont: true,       // true to make merror text use surrounding font
    mathmlSpacing: false,          // true for MathML spacing rules, false for TeX rules
    skipAttributes: {},            // RFDa and other attributes NOT to copy to the output
    exFactor: .5,                  // default size of ex in em units
    displayAlign: 'center',        // default for indentalign when set to 'auto'
    displayIndent: '0',            // default for indentshift when set to 'auto'
    fontCache: 'local',            // or 'global' or 'none'
    localID: null,                 // ID to use for local font cache (for single equation processing)
    internalSpeechTitles: true,    // insert <title> tags with speech content
    titleID: 0                     // initial id number to use for aria-labeledby titles
  }
};

// document$.subscribe(() => {
// //   MathJax.typesetClear()
// //   MathJax.texReset()
//   MathJax.typesetPromise()
// })
