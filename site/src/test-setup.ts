import "@testing-library/jest-dom/vitest";

// jsdom does not implement smooth scrolling
if (typeof Element !== "undefined" && !Element.prototype.scrollTo) {
  Element.prototype.scrollTo = () => {};
}
