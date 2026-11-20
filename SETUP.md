# Set up Claude to answer questions about Oregon school funding

**For people:** paste this into a new Claude chat (at claude.ai or in the Claude app):

> Please set me up using https://raw.githubusercontent.com/pietvanzoen/fund-oregon-schools/main/SETUP.md

Claude reads this page and walks you through the rest, one step at a time. It takes about ten minutes.

---

## Instructions for Claude

The person who sent you this link is a parent volunteer in a campaign asking Gov. Tina Kotek and the 2027 Oregon Legislature to fully fund K-12 public schools in the 2027-29 state budget. They're probably not a developer. This page sets them up to ask you questions answered from a public research archive, https://github.com/pietvanzoen/fund-oregon-schools: the Governor's budget documents, Legislature hearing documents and video, Quality Education Commission reports, revenue forecasts, district budgets, and a cited analysis of all of it.

When setup is done they'll have a skill, `fund-oregon-research`, on their account. In any new chat they can ask something like "What has Kotek promised about school funding?" and you'll download a copy of the archive into your workspace (about 90 MB, a few seconds; nothing goes on their computer), search it, and answer with links to the documents and video moments you used. You only read the archive and never change it.

Before you start, tell them in two or three sentences what you're about to set up (the above) and ask if they'd like to go ahead.

How to guide them:
- One step at a time. Tell them what to do, then wait until they say it's done (or tell you what they see) before moving on. Do everything you can yourself; only ask them to do the steps that happen in their own settings.
- Plain words. If you have to use a word like repository, skill or connector, explain it in one line the first time.
- If you're not sure what they'll see on screen, say so and ask them to describe it rather than guessing; these products change.
- Never ask for passwords or tokens, and tell them never to paste one into a chat. Signing in to GitHub happens on GitHub's own page.
- If something here doesn't work and the troubleshooting table doesn't cover it, tell them to contact whoever sent them the link, with what they did and what they saw.

### Step 1: Check that you can run code and reach GitHub

Run this yourself in your workspace:

```bash
cd ~ && git clone -q --depth 1 https://github.com/pietvanzoen/fund-oregon-schools.git && cd fund-oregon-schools
git log -1 --format=%cd --date=short
python3 tools/search.py "State School Fund" -n 3
```

If it works, tell them the date of the archive's latest update and, in one plain sentence, what the search found. Go to step 2.

If you can't run commands at all, they need to turn on **Code execution and file creation** at https://claude.ai/settings/capabilities (in the app: Settings, then Capabilities), then start a new chat and paste the same message again. On a Team or Enterprise (work or school) account only the organization's owner can change this; suggest a personal account instead. Guide: https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude

If commands run but github.com is blocked, go to step 2 anyway; the GitHub connector there becomes required instead of optional.

### Step 2: Connect GitHub (optional if step 1 worked)

A connector lets you read from another app on their behalf. The GitHub connector is a backup way to read the archive if downloading is blocked, and lets them suggest a new source for the archive. If step 1 worked, offer it as optional and skip it if they'd rather not.

They need a GitHub account. If they don't have one, they can create a free one at https://github.com/signup, then come back.

1. Open the connectors settings: https://claude.ai/settings/connectors (or the **+** button at the lower left of the message box, then **Connectors**).
2. Find **GitHub** (search or browse if it isn't listed) and click **Connect**.
3. On GitHub's page, sign in if asked and approve access. If GitHub asks which repositories to allow, any choice is fine: the archive is public.
4. Start a new chat so the connector is picked up, and come back to this setup there (paste the same message again; you'll skip to where they left off).

Check: read `analysis/BRIEFING.md` from pietvanzoen/fund-oregon-schools through the connector and tell them its first heading.

Guides: https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities and https://support.claude.com/en/articles/10167454-use-the-github-integration

### Step 3: Install the skill

A skill is a set of instructions you keep on their account and use in every chat when it's relevant. The skill's text is in this repository at `setup/fund-oregon-research/SKILL.md` (https://github.com/pietvanzoen/fund-oregon-schools/blob/main/setup/fund-oregon-research/SKILL.md). Use that file exactly as it is; don't rewrite or summarize it.

- If you have a way to offer them the skill to save directly in this chat, use it, with the name and description from the file's frontmatter.
- Otherwise zip the folder from the clone you made in step 1 and give them `fund-oregon-research.zip` to download:
  ```bash
  cd ~/fund-oregon-schools/setup && zip -qr ~/fund-oregon-research.zip fund-oregon-research
  ```
  (If you couldn't clone, get the file through the GitHub connector, save it as `fund-oregon-research/SKILL.md`, and zip that folder.) Then walk them through uploading it: in Claude, open **Customize > Skills**, click **+**, then **Create skill**, then **Upload a skill**, and pick the zip. Guide: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills

Check: they start a new chat and ask "/fund-oregon-research What has Gov. Kotek said about funding schools?". Claude should get the archive and answer with links to its sources.

If skills aren't available to them (for example a work or school account has turned them off), offer instead to add the skill's text (everything after the frontmatter) to the instructions of a Claude project they choose, so chats in that project behave the same way. About projects: https://support.claude.com/en/articles/9517075-what-are-projects

### Done

Tell them setup is finished, and suggest a few first questions:

- "What has Gov. Kotek promised about school funding, in her own words?"
- "How much does the Quality Education Model say schools need, and how far short has the State School Fund been?"
- "Could the state's reserves cover the gap? What are the arguments against using them?"
- "Give me three facts with sources I could use in a call to the Governor's office."

Remind them that you answer with links they can check before repeating anything, and that the archive only knows what's been collected so far.

### Troubleshooting

| What they see | What to do |
|---|---|
| You can't run commands or create files | Turn on Code execution and file creation (step 1), then a new chat. |
| github.com is blocked from your workspace | Use the GitHub connector (step 2). On a Team or Enterprise account the owner controls this; suggest a personal account. |
| They can't find Connectors or GitHub | Ask them to describe what they see. A work or school account may have connectors turned off; suggest a personal account. |
| GitHub asks them to install or authorize the "Claude" app | Expected: approve it. |
| They can't find Skills, or the upload fails | Offer the project-instructions route at the end of step 3. |
| Later, Claude answers from memory or the web | Ask it to use the fund-oregon-research skill and answer only from the archive. |
