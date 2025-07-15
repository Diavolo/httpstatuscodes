# [httpstatuscodes.org][9]

[httpstatuscodes.org][9] is an easy to reference database of HTTP Status Codes with their definitions and helpful code references, each code is at `httpstatuscodes.org/code`. All standard codes are included, as are some non-standard codes that have significant presence in the wild.

## Technology Stack

This project is built with:
- **Flask** - Python web framework
- **Frozen-Flask** - Static site generator
- **Tailwind CSS** - Utility-first CSS framework
- **Markdown** - Content format for status codes

## Development Setup

To build and run this project locally:

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Build CSS assets:**
   ```bash
   npm run build
   ```

4. **Run the development server:**
   ```bash
   flask --app app run --debug
   ```

5. **For development with CSS watching:**
   ```bash
   npm run dev
   ```

## Deployment Options

This project can be deployed in two ways:

### Option 1: Flask Application

Deploy as a traditional Flask web application:

1. **Build production CSS:**
   ```bash
   npm run prod
   ```

2. **Run with Gunicorn (production WSGI server):**
   ```bash
   gunicorn --workers 4 --bind 0.0.0.0:8000 main:app
   ```

3. **Or run with Flask development server:**
   ```bash
   flask --app main run --debug
   ```

### Option 2: Static Site Generation

Generate a static site for deployment to CDN or static hosting:

1. **Build production CSS:**
   ```bash
   npm run prod
   ```

2. **Generate static site:**
   ```bash
   python freezer.py
   ```

3. **Deploy the generated `build/` directory** to your static hosting provider (Netlify, Vercel, GitHub Pages, etc.)

## Contributing

All contributions are welcome! If you have an idea to improve the website please submit a pull request or [create an issue][1], or provide your thoughts on [open issues][1].

Each status code lives in a Markdown file at [app/contents/codes](app/contents/codes), the easiest way to submit changes is via the GitHub editor. When contributing changes to the status codes please be mindful of the following:

* Markdown links should be used as [references instead of inline][2]
* If an RFC or external document is referenced, make the reference a link
* Source information on a status code from the most recent standards available (Status Code standards directory is available on [iana.org][3])
* The opening paragraph of a status code should describe the meaning, following paragraphs can describe implementation
* Don't edit the meaning of descriptions, but formatting and structural changes are a-okay
* [Don't double-space after a period][4], and remove any examples of it
* If the description references a section in the current RFC, always add the RFC identifier. For example "Section 6.6" should become "RFC1234 Section 6.6"

## Project History

This project was originally known as [httpstatus.es][6] but [as per this GitHub issue][7] migrated to [httpstatuses.com][5] in November 2015 for SEO reasons.

**Current Status of Original Project:**
The original httpstatuses.com is no longer available as a reference site - it now redirects to a commercial website. The original repository has been transferred to a new owner but remains inactive since November 2016.

**This Project:**
This is a hobby project rebuilt from scratch with modern technologies (Flask and Tailwind CSS) with the intention to revive and maintain the HTTP status codes reference that was previously available. The goal is to provide the same valuable resource that the original project offered, but with updated technology and active maintenance.

The project is maintained at [github.com/Diavolo/httpstatuscodes][8].

[1]: <https://github.com/Diavolo/httpstatuscodes/issues>
[2]: <https://daringfireball.net/projects/markdown/syntax#link>
[3]: <http://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml>
[4]: <http://www.slate.com/articles/technology/technology/2011/01/space_invaders.html>
[5]: <https://httpstatuses.com>
[6]: <https://httpstatus.es>
[7]: <https://github.com/citricsquid/httpstatuses/issues/29>
[8]: <https://github.com/Diavolo/httpstatuscodes>
[9]: <https://httpstatuscodes.org>
