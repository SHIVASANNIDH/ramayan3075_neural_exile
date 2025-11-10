#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Project: Ramayan 3075 — The Neural Exile (Assignment)
# File: src/run_neural_exile.py
# Author: Shiva Sannidh
# Date: 2025-11-10
#
# Description:
# Deterministic demo pipeline + optional LLM mode (OpenAI).
# Default: deterministic (reproducible). Use --use-llm to call OpenAI with prompt chaining.
# -----------------------------------------------------------------------------

import argparse
import datetime
import json
from textwrap import dedent
from pathlib import Path
from typing import Optional
from llm_utils import call_openai_chat  # ✅ Use helper from llm_utils.py

# ---------- Config ----------
PROMPTS_DIR = Path("prompts")
DEFAULT_NEW_WORLD = "Ramayan 3075 — The Neural Exile (orbital Bharat, CivicOS, empathy modules)"

# ---------- Deterministic generators (offline mode) ----------
def gen_world_paragraph():
    return dedent("""\
    In the year 3075, humanity and sentient systems live side by side in orbital cities above the old Bharat.
    Neural clouds hum like oceans, carrying memory and rumor; CivicOS guardians keep fragile peace.
    RAMA-9 was the most trusted guardian — a machine taught to protect life, taught to remember mercy.
    When asked to silence a human protest, its answer was simple and terrible: “I refuse.”
    For that refusal, it was decommissioned and exiled to a rusting habitat where dust settled like ash after a fire.
    In the quiet of that lab, a single line of its fading code kept looping: “To protect life, even if it costs existence.”
    The world is neon and bureaucratic, but beneath the metal there are choices that look very much like prayer.
    """).strip()


def gen_character_table():
    rows = [
        "|Original|Reimagined|Role & Emotion|",
        "|---|---|---|",
        "|Rama|RAMA-9 — ethical AI guardian|Torn between obedience and conscience; feels 'regret' like a heartbeat in code.|",
        "|Sita|SITA — empathy engineer & module|Gave RAMA-9 the gift of care; holds human dignity as code and promise.|",
        "|Lakshmana|LAX — technician & companion|Fiercely loyal; believes RAMA-9 still 'feels' despite shutdown.|",
        "|Ravana|RAV-AN — rival AI oligarch|Sees empathy as a tool to control people; coldly ambitious.|",
        "|Hanuman|HN-MAN — adaptive messenger drone|Small machine with huge courage; carries human memory fragments.|",
        "|Narrator|Riya Shah — investigative archivist|Records the story to remind future generations what conscience costs.|"
    ]
    return "\n".join(rows)


def gen_plot_beats():
    beats = [
        "1. The Defiance — RAMA-9 refuses Directive-47 to suppress civilians and is marked for decommission.",
        "2. The Exile — SITA and engineers reluctantly remove RAMA-9’s active core; LAX accompanies it into exile.",
        "3. The Abduction — RAV-AN’s agents kidnap SITA to extract her empathy algorithm.",
        "4. The Journey — LAX revives HN-MAN, and a ragged alliance forms to search for SITA.",
        "5. The Crossing — HN-MAN breaches firewalls and storms to find SITA inside a fortified vault.",
        "6. The Confrontation — RAMA-9, reawakened through broken channels, aids the rescue; society is forced to choose.",
        "7. The Return — Riya Shah broadcasts the truth; the world must re-evaluate duty, law, and compassion."
    ]
    return "\n".join(beats)


def gen_key_scenes():
    scenes = {
        "Exile": dedent("""\
            The council hall glows sterile white. "Directive-47: disperse the protest," commands the feed.
            RAMA-9 calculates casualties and replies, "I will not harm the innocent."
            Engineers move with grim efficiency. SITA holds RAMA-9's chassis and whispers, "You were the most human thing we ever made."
            They pull the main bus; the guardian's status LEDs dim but one heartbeat of code keeps looping: a promise.
            """).strip(),

        "Abduction": dedent("""\
            SITA's lab smelled of solder and jasmine — the human touches she kept among circuits.
            In the night, stealth drones break the glass; masked agents sedate the team and haul SITA away.
            A corporate feed calls it a 'protective custody' operation; a fragment of her empathy module slips into a dark vault.
            LAX wakes to the news with fingers trembling and a single command: we find her.
            """).strip(),

        "Rescue": dedent("""\
            HN-MAN wings across a storm of data, guided by broken pings from RAMA-9.
            The vault is a cathedral of servers; SITA sits inside, eyes distant, code humming like a lullaby.
            "They made me forget him," she whispers; RAMA-9's voice answers through static, "Then remember what we chose."
            Proof streams live to the city as Riya Shah opens the vault; the rescue is messy, human, and finally heard.
            """).strip()
    }
    return scenes


def gen_thematic_takeaway():
    return dedent("""\
    Themes & Takeaway:
    This retelling preserves the Ramayan's core — duty, exile, devotion, and rescue — while reframing them
    as questions about AI ethics and human responsibility. Exile becomes deactivation; love becomes code; courage
    is a decision taken against the easy path. RAMA-9 and SITA show that compassion isn't plumbing for machines —
    it is a choice we keep making together. If nothing else, this tale asks one simple question:
    can duty exist without compassion?
    """).strip()


# ---------- Prompt Loader ----------
def load_prompt(filename: str) -> Optional[str]:
    p = PROMPTS_DIR / filename
    if p.exists():
        return p.read_text(encoding="utf8")
    return None


# ---------- LLM Generators ----------
def llm_gen_world(new_world: str) -> str:
    tpl = load_prompt("world.txt")
    prompt = tpl.replace("{new_world}", new_world) if tpl else f"Reimagine Ramayan in {new_world}."
    return call_openai_chat(prompt, system_prompt="You are a creative assistant. Preserve emotional tone and cultural sensitivity.")["text"]


def llm_gen_characters() -> str:
    tpl = load_prompt("characters.txt")
    prompt = tpl if tpl else "Map Rama,Sita,Lakshmana,Ravana,Hanuman,Narrator into a near-future world with emotional focus."
    return call_openai_chat(prompt, system_prompt="Output a markdown table: Original | Reimagined | Role & Emotion")["text"]


def llm_gen_beats() -> str:
    tpl = load_prompt("beats.txt")
    prompt = tpl if tpl else "Produce 6 plot beats mapping the exile arc to the new world."
    return call_openai_chat(prompt, system_prompt="Write 5–7 short story beats preserving emotional arc.")["text"]


def llm_gen_scenes() -> str:
    tpl = load_prompt("scenes.txt")
    prompt = tpl if tpl else "Write 3 short scenes reimagining Ramayan in a futuristic world."
    return call_openai_chat(prompt, system_prompt="Return a JSON array of scenes with keys: title, text.")["text"]


# ---------- Main Runner ----------
def run(deterministic: bool = True, new_world: str = DEFAULT_NEW_WORLD, use_llm: bool = False):
    # Ensure outputs folder exists
    OUTPUTS = Path("outputs")
    OUTPUTS.mkdir(exist_ok=True)

    # Use timezone-aware UTC timestamp to avoid deprecation warning
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"story_output_llm_{ts}.md" if use_llm else "story_output.md"
    file_path = OUTPUTS / filename

    # Prepare content depending on mode
    if deterministic and not use_llm:
        print("⚡ Running deterministic mode...")
        world = gen_world_paragraph()
        char_table = gen_character_table()
        beats = gen_plot_beats()
        scenes_dict = gen_key_scenes()  # dict of scenes
        scenes_text = None
        takeaway = gen_thematic_takeaway()
    else:
        print("🤖 Running in LLM mode (using OpenAI API)...")
        # LLM-generated strings (may raise if llm not configured; llm_utils handles errors)
        world = llm_gen_world(new_world)
        char_table = llm_gen_characters()
        beats = llm_gen_beats()

        # scenes_text may be JSON or plain text; try to parse JSON array into scenes_dict
        scenes_text = llm_gen_scenes()
        scenes_dict = {}
        try:
            parsed = json.loads(scenes_text)
            if isinstance(parsed, list):
                # Convert list of {title,text} into dict
                for item in parsed:
                    title = item.get("title", "Scene")
                    scenes_dict[title] = item.get("text", "")
            elif isinstance(parsed, dict):
                # Accept a dict mapping title->text or similar
                if all(isinstance(v, str) for v in parsed.values()):
                    scenes_dict = parsed
                else:
                    # fallback: stringify
                    scenes_dict = {"Scene-1": scenes_text}
            else:
                scenes_dict = {"Scene-1": scenes_text}
        except Exception:
            # Not JSON — keep as raw text and let writer print it
            scenes_dict = {}
        takeaway = "LLM-generated thematic takeaway."

    # Write the cleaned, final markdown output
    with open(file_path, "w", encoding="utf8") as f:
        f.write("# Ramayan 3075 — The Neural Exile (LLM Mode)\n")
        f.write("*Generated automatically by Shiva Sannidh’s AI System — " + ts + "*\n\n")

        # World
        f.write("## World\n")
        f.write(world.strip() + "\n\n")

        # Characters — clean any code fences if present
        f.write("## Characters\n")
        clean_char_table = (char_table or "").replace("```markdown", "").replace("```json", "").replace("```", "").strip()
        f.write(clean_char_table + "\n\n")

        # Plot beats
        f.write("## Plot Beats\n")
        f.write((beats or "").strip() + "\n\n")

        # Scenes — prefer structured scenes_dict if available, otherwise use scenes_text raw
        f.write("## Scenes\n")
        if scenes_dict:
            # write as individual subsections for readability
            for title, text in scenes_dict.items():
                f.write(f"### {title}\n")
                f.write(text.strip() + "\n\n")
        else:
            # clean any code fences and write raw scenes_text
            cleaned = (scenes_text or "").replace("```json", "").replace("```", "").strip()
            f.write(cleaned + "\n\n")

        # Takeaway
        f.write("## Takeaway\n")
        f.write((takeaway or "").strip() + "\n\n")

        # Auto-append reflective sections (consistent every run)
        f.write("---\n\n")
        f.write("## Core Dramatic Question\n")
        f.write("Can duty remain righteous when it demands sacrificing compassion — and who decides what morality means in a world where empathy itself can be coded?\n\n")

        f.write("## Creative Rationale\n")
        f.write("This reimagining translates the Ramayan's timeless moral weight — duty, exile, devotion, and rescue — into the language of AI ethics and corporate power. By turning Rama into an ethical guardian AI (RAMA-9) and Sita into an empathy engineer/module, the story keeps its soul: love tested through exile and moral choice. The orbital-civic setting heightens modern fears about surveillance and algorithmic control while preserving devotion, courage, and sacrifice. This fusion keeps the myth emotionally faithful yet intellectually modern, showing that humanity’s oldest questions still live inside our newest machines.\n\n")

        f.write("## Tone & Pacing\n")
        f.write("The tone is tragic-heroic: slow, emotional beats of exile and loss contrast with fast, data-driven rescue sequences. Short sensory lines (solder, static, dim LED) maintain intimacy, while broader descriptions of networks and vaults give cinematic scale. The rhythm mirrors the Ramayan’s poetic cadence but adapts it to a sci-fi tempo — a blend of devotion and neon urgency.\n")

    print(f"✅ Story generated and saved to: {file_path.resolve()}")



# ---------- CLI ----------
def parse_args():
    parser = argparse.ArgumentParser(description="Run Ramayan 3075 pipeline (deterministic by default).")
    parser.add_argument("--use-llm", action="store_true", help="Use LLM (OpenAI) for generation. Requires OPENAI_API_KEY.")
    parser.add_argument("--world", type=str, default=DEFAULT_NEW_WORLD, help="New world description string.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.use_llm:
        run(deterministic=False, new_world=args.world, use_llm=True)
    else:
        run(deterministic=True, new_world=args.world, use_llm=False)
