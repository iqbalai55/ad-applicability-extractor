# Businees Context
Hundreds of new ADs monthly come. Manual extraction doesn't scale, so we need automated pipelines that can reliably extract applicability rules from PDF documents. So we can answer  "Is aircraft X affected by AD Y?" or "what AD that affected the aircraft" easily.

# Problem

When extracting applicability rules from AD documents, there is no fixed or consistent structure that allows for purely rule-based extraction. For example, FAA ADs in the applicability section typically use numbered lists to specify aircraft models, such as (1) Model MD-11, (2) Model MD-10-10F, and so on. In contrast, EASA ADs are more narrative, listing aircraft models in long sentences with commas and the word “and.” Therefore, a flexible algorithm is required to handle this variation effectively.

# Approach

There are several approaches we can use: LLM API, fine-tuning an LLM, and VLMs. Using the LLM API seems the easiest and best fits our needs because it excels at general reasoning and can extract or parse information directly using prompt instructions, without relying on rigid rules. Fine-tuning could also achieve this, but it typically requires a large amount of training data, which doesn’t suit current test with only two documents. VLMs are also an interesting approach, particularly systems like DeepSeek-OCR, which can convert documents into visual representations and claim to reduce token usage. However, for practicality, we use the LLM api.

Feeding the entire AD document to an LLM is very inefficient because ADs also contain inspection procedures and other details, which would consume a lot of tokens unnecessarily.

###  Step 1: Extracting the Applicability Section
Therefore, the first step is to extract the Applicability section before sending it to the LLM. This is done by locating the “Applicability” header and capturing all text that follows, stopping at a clear separation like a double line break or the end of the document.

To detect the header in plain text, the logic looks for cues such as short prefixes or numbering before the word (e.g., (c), (1)), small suffixes after it (like a colon), and the presence of the word “Applicability” itself. 

Although this section extraction is not perfect, particularly for determining its end because newlines (as our stop sign) can become messy during text extraction, sometimes the next section may be partially included. Still, it is much more efficient than feeding the entire document to the LLM. You can run "test/test_extract_applicability_section.py" file to see the ouput.

So, if there is extra time, we must refine this regex rule.

###  Step 2: Parsing the Extracted Section

After extraction, we feed this result into our agent that we prompt to parse to the folowing stucture:

```json
{
  "ad_id": "FAA-2025-23-53",
  "applicability_rules": {
    "aircraft_models": ["MD-11", "MD-11F"],
    "msn_constraints": null,
    "excluded_if_modifications": ["SB-XXX"],
    "required_modifications": []
  }
}
```

I don’t modify this structure since, according to the two provided AD documents, this is already sufficient, with the assumption that each modification only applies to the aircraft models explicitly listed. This means that when a user inputs a combination of aircraft model and modification, the system can correctly determine which AD is affected or not. Each model’s modifications are independent, so no modification for one model will apply to or exclude another model. This keeps the parsing simple while maintaining correct mapping between models and modifications.

For example, the Airbus A320-211 is included in the AD unless it has mod 24591 or the relevant service bulletin, while mod 24977 only applies to the Airbus A321. Under this assumption, the system does not expect a user to input a combination like A320-211 with mod 24977.

If there is such behaviour (the edge case), separate applicability rules would be required for each AD to ensure accurate mapping of modifications to models and to maintain precise determination of which aircraft are affected. And I hope I can add this if there is extra time.

### Step 3: Prompt Refinement and Testing
I refined the prompt itself based on a feedback loop from the LLM results. That’s why I created the file test\test_extraction_agent.py, to identify where the extraction mismatches or deviates from the expected output, so I can iteratively improve the prompt and parsing accuracy, for now, i just manually refine it, but it can be automated with agent-eval pattern.

The optimized prompt rule is only tuned for these two AD documents, so it’s a very limited scope. I believe a feedback loop with many more documents is necessary to generalize the extraction logic effectively

Afterward, I tested several combinations, and the results are summarized in the following table: 

| Aircraft       | MSN   | Modification                 | FAA AD 2025-23-53 | EASA AD 2025-0254 |
|:---------------|:------|:-----------------------------|:------------------|:------------------|
| MD-11          | 48123 | None                         | Affected          | Not affected      |
| DC-10-30F      | 47890 | None                         | Affected          | Not affected      |
| Boeing 737-800 | 30123 | None                         | Not affected      | Not affected      |
| A320-214       | 5234  | None                         | Not affected      | Affected          |
| A320-232       | 6789  | mod 24591       | Not affected      | Not affected      |
| A320-214       | 7456  | SB A320-57-1089 Rev 04       | Not affected      | Not affected      |
| A321-111       | 8123  | None                         | Not affected      | Affected          |
| A321-112       | 364   | mod 24977      | Not affected      | Not affected      |
| A319-100       | 9234  | None                         | Not affected      | Not affected      |
| MD-10-10F      | 46234 | None                         | Affected          | Not affected      |

An aircraft is considered affected by an AD only if it passes all applicability checks in order: it must match a listed aircraft model, fall within any specified serial number constraints, have no excluded modifications (such as certain production mods or service bulletins), and —if required— possess the necessary modifications. The evaluation stops at the first failing condition: a mismatched model, an out-of-range MSN, or a disqualifying modification immediately excludes the aircraft.

I also check too and it pass below table. 

| Aircraft    | MSN   | Modifications             | FAA AD 2025-23-53 | EASA AD 2025-0254 |
|:------------|:------|:--------------------------|:------------------|:------------------|
| MD-11F      | 48400 | None                      | ✅ Affected       | ❌ Not Affected |
| A320-214    | 4500  | mod 24591    | ❌ Not Affected | ❌ Not affected   |
| A320-214    | 4500  | None                      | ❌ Not Affected | ✅ Affected       |

