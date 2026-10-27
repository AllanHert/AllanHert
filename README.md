<!-- Generated from profile.yaml by scripts/build_readme.py. Edit profile.yaml, not this file. -->

<img src="./assets/banner.png" alt="Allan Hert, software engineer: full-stack and AI. Open to remote roles, São Paulo, UTC-3." width="100%" />

<p align="center">
  <a href="https://allanhert.com">allanhert.com</a>
  ·
  <a href="https://www.linkedin.com/in/allanhert">LinkedIn</a>
  ·
  <a href="https://x.com/HertAllan">X</a>
  ·
  <a href="mailto:allanhert@gmail.com">Email</a>
  ·
  <a href="https://hertwave.com">Hertwave</a>
</p>

## About

I build software end to end: the product decision, the architecture, the interface, the deploy and the fix two months later.
Most days that means **TypeScript and Next.js** on the web, **Python** for automation and data, and **LLM agents** wired into real workflows with tests and human checkpoints.

I run [Hertwave](https://hertwave.com), a small studio in São Paulo that ships sites and software for real clients. I'm also finishing a law degree at Mackenzie, which shapes how I scope anything that touches personal data or a contract.

Most of my work lives in private repositories. Below are case studies that explain what each product does, how it is built and what I decided, plus the code I keep public.

---

## Selected products

### quemapoiaquem

<p>
  <a href="https://quemapoiaquem.com.br"><img src="./assets/previews/quemapoiaquem.jpg" alt="quemapoiaquem preview" width="100%" /></a>
</p>

A neutral public record of who backed whom in Brazil's 2026 presidential runoff, every endorsement linked to its source. Started on 2026-10-05, live the next day, frozen after the vote: 74,000 visits and about 518,000 views on X by 2026-10-25.

**Focus:** Zero to production in one day · AI triage with human review · Neutrality rules enforced in the data model  
**Stack:** Next.js · TypeScript · Postgres (Neon) · Cloudflare R2 · Playwright · Claude

<a href="https://quemapoiaquem.com.br"><strong>Live product →</strong></a> &nbsp;·&nbsp; <a href="https://github.com/AllanHert/quemapoiaquem"><strong>Case study →</strong></a>


### Valor de Imóveis

<p>
  <a href="https://valordeimoveis.com.br"><img src="./assets/previews/valor-imoveis.jpg" alt="Valor de Imóveis preview" width="100%" /></a>
</p>

The platform behind a live real-estate agency: public site, admin, watermarked photos, XML feeds to Brazil's major listing portals and a CRM. Built multi-tenant from the schema up, with Postgres row-level security.

**Focus:** Full-stack platform · Portal integrations · Tenant isolation  
**Stack:** Next.js · TypeScript · Supabase / Postgres · Cloudflare R2 · Vercel AI Gateway

<a href="https://valordeimoveis.com.br"><strong>Live product →</strong></a> &nbsp;·&nbsp; <a href="https://github.com/AllanHert/valor-imoveis"><strong>Case study →</strong></a>


---

## AI systems and internal tools

<table>
  <tr>
    <td width="56" align="center"><img src="./assets/icons/voice.svg" width="40" alt="" /></td>
    <td><a href="https://github.com/AllanHert/jarvis"><strong>Jarvis</strong></a><br/>Local-first voice assistant for Windows: Whisper wake word, local TTS, Claude Code acting on the PC through typed MCP tools that ask for confirmation.<br/><sub>Python · Claude Code + MCP · faster-whisper · Tauri + React · Ollama · SQLite</sub></td>
  </tr>
  <tr>
    <td width="56" align="center"><img src="./assets/icons/factory.svg" width="40" alt="" /></td>
    <td><a href="https://github.com/AllanHert/hertwave-os"><strong>Hertwave OS</strong></a><br/>The studio's agent factory: Claude Code agents build client sites, a critic scores each render on a 9-part rubric and a fix is kept only if the score rises.<br/><sub>Claude Code agents · Node.js · Playwright · Next.js · Tailwind v4</sub></td>
  </tr>
  <tr>
    <td width="56" align="center"><img src="./assets/icons/contract.svg" width="40" alt="" /></td>
    <td><a href="https://github.com/AllanHert/contratos"><strong>Contratos</strong></a><br/>Turns property records and ID scans into full real-estate contracts: 13 types, faithful to the agencies' own templates, with a human check on the deal sheet before the .docx.<br/><sub>Python · Claude · JSON Schema · docxtpl</sub></td>
  </tr>
  <tr>
    <td width="56" align="center"><img src="./assets/icons/research.svg" width="40" alt="" /></td>
    <td><a href="https://github.com/AllanHert/quant-research"><strong>Quant research</strong></a><br/>Systematic research for crypto and US equities: hypotheses registered before testing, a sealed holdout, a blind reviewer agent and paper trading with no orders.<br/><sub>Python · Polars · statsmodels · pytest + Hypothesis · Claude Code agents</sub></td>
  </tr>
</table>

## Sites shipped for clients and the studio

| Site | What it shows |
|---|---|
| [hertwave.com](https://hertwave.com) | Studio site: GLSL hero, 3D carousel in React Three Fiber, PT/EN. |
| [nowimoveis.com](https://nowimoveis.com) | Video-first real estate: each YouTube tour becomes a property page in chapters, scroll drives the playhead. |
| [nowmarketing.com.br](https://nowmarketing.com.br) | Agency site with a 3D opening scored to scroll. |
| [oktal.com.br](https://oktal.com.br) | Tech gadget store built as a studio portfolio piece. |
| [jimmyk.com.br](https://www.jimmyk.com.br) | One-page site for an old-school barbershop, built to drive WhatsApp bookings. |

## Public source

<table>
  <tr>
    <td width="56" align="center"><img src="./assets/icons/webgl.svg" width="40" alt="" /></td>
    <td><a href="https://github.com/AllanHert/allanhert-portfolio"><strong>allanhert-portfolio</strong></a><br/>My site and WebGL lab: GPU reaction-diffusion, SDF raymarching and ordered dithering, each one a hand-written shader.<br/><sub>Next.js · Three.js · GLSL · Playwright</sub></td>
  </tr>
</table>

---

## Toolkit

<p>
  <img src="https://skillicons.dev/icons?i=ts,js,react,nextjs,nodejs,python,postgres,tailwind,threejs,vercel,git,linux&theme=dark" alt="Main technologies" />
</p>

**Languages:** TypeScript · JavaScript · Python · SQL · GLSL  
**Web:** React · Next.js · Node.js · Tailwind · Three.js / React Three Fiber  
**Data and infra:** Postgres · Neon · Supabase · Vercel · Linux VPS  
**AI:** Claude Code agents · MCP servers · LLM extraction pipelines · local speech (Whisper, TTS)  
**Quality:** Playwright · pytest · Vitest · axe-core  

## How I work

- Start from the real problem and the person using it, then pick the smallest thing that can go live.
- Write the decision down before the code: each project keeps its plan, phases and decision log in the repo.
- Agents do the heavy lifting, people approve anything irreversible: payments, messages, publishing.
- Test what can break, measure what ships, and keep secrets and personal data out of git.

---

<sub>Most client work is private. Case studies describe it without the source.</sub>
