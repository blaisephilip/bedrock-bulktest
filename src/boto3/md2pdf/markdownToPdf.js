import { marked } from 'marked'; // Add marked package for Markdown parsing
import highlightjs from 'highlight.js'; // Add highlight.js for code highlighting
import puppeteer from 'puppeteer';
import { promises as fs } from 'fs';
import {setTimeout} from "node:timers/promises";
import plantumlEncoder from 'plantuml-encoder';  // Add this import

async function markdownToPdf(markdownPath, pdfPath) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Read the Markdown file
    const markdownContent = await fs.readFile(markdownPath, 'utf-8');

    // Configure marked with syntax highlighting
    marked.setOptions({
        highlight: function(code, lang) {
            return highlightjs.highlight(code, { language: lang }).value;
        }
    });

    // Convert Markdown to HTML
    //             <!-- <title>Markdown to PDF</title> -->
    const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css">
            <script src="https://cdn.jsdelivr.net/npm/plantuml-encoder@1.4.0/dist/plantuml-encoder.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/kroki-js@0.2.0/dist/kroki.min.js"></script>
            <style>
                body { 
                    font-family: sans-serif;
                    margin: 40px;
                    line-height: 1.6;
                }
                pre code {
                    background-color: #f6f8fa;
                    border-radius: 6px;
                    padding: 16px;
                    display: block;
                }
                .plantuml-diagram {
                    text-align: center;
                    margin: 20px 0;
                }
                img {
                    max-width: 100%;
                    height: auto;
                }
                .pageNumber {
                    position: fixed;
                    bottom: 10px;
                    right: 10px;
                    font-size: 12px;
                }
                /* Hide page numbers during generation */
                @media screen {
                    .pageNumber {
                        display: none;
                    }
                }
            </style>
        </head>
        <body>
            ${await processMarkdown(markdownContent)}
        </body>
        </html>
    `;

    await page.setContent(htmlContent);

    // Wait for PlantUML diagrams to render
    await page.waitForFunction(() => {
        const images = document.getElementsByTagName('img');
        return Array.from(images).every(img => img.complete);
    });
    
    // Additional wait to ensure diagrams are fully rendered
    await setTimeout(3000);

    await page.pdf({
        path: pdfPath,
        format: 'A4',
        printBackground: true,
        margin: {
            top: '20mm',
            right: '20mm',
            bottom: '20mm',
            left: '20mm'
        },
        displayHeaderFooter: true,
        footerTemplate: `
            <div style="width: 100%; font-size: 10px; padding: 0 20px; text-align: right;">
                <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
            </div>
        `
    });

    await browser.close();
}

async function processMarkdown(content) {
    // Process PlantUML blocks
    content = content.replace(/```plantuml([\s\S]*?)```/g, (match, diagram) => {
        const encoded = plantumlEncoder.encode(diagram.trim());
        return `<div class="plantuml-diagram">
            <img src="https://www.plantuml.com/plantuml/svg/${encoded}" alt="PlantUML diagram">
        </div>`;
    });

    // Convert the rest of the markdown
    return marked(content);
}

const markdownPath = process.argv[2];
const pdfPath = process.argv[3];

if (!markdownPath || !pdfPath) {
    console.error('Usage: node markdown-to-pdf.js <markdown_file_path> <pdf_file_path>');
    process.exit(1);
}

markdownToPdf(markdownPath, pdfPath).catch(err => {
    console.error('Error:', err);
    process.exit(1);
});