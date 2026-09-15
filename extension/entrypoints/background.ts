export default defineBackground(() => {
    // Clicking the toolbar icon opens the side panel.
    void chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
});
