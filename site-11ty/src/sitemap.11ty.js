// Every page but search and 404, for search engines
export const data = { permalink: "/sitemap.xml" };
export const render = ({ archive }) => `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${["/", ...archive.pages.map((p) => p.url)].map((u) => `<url><loc>https://oregonedtrail.org${u}</loc></url>`).join("\n")}
</urlset>
`;
