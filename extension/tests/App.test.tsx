import { render, screen } from "@testing-library/react";

import { App } from "../entrypoints/sidepanel/App";

test("renders the heading", () => {
    render(<App />);
    expect(screen.getByRole("heading").textContent).toBe("Hello");
});
