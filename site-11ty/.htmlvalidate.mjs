export default {
  extends: ["html-validate:recommended"],
  rules: {
    // the funding chart's bar widths come from the data, so they're set inline; the site sets no CSP that forbids it
    "no-inline-style": "off",
    // whitespace left by the templates and Markdown; readers and screen readers never see it
    "no-trailing-whitespace": "off",
    // titles follow CLAUDE.md rule 4 (at most 55 characters) plus " · Oregon Ed Trail"; this rule counts entities raw
    "long-title": "off",
  },
};
