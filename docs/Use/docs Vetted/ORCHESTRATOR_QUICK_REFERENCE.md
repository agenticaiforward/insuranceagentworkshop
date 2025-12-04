# 🎨 Orchestrator Quick Reference Card
**AI Studio Cheat Sheet - No Coding Required!**

---

## 🚀 Getting Started (5 min)

**1. Get API Key**
- Go to: https://aistudio.google.com/
- Click "Get API Key" → Create new key
- Copy and save it (starts with `AIza...`)

**2. Open AI Studio**
- Click "Create new prompt"
- Choose "Freeform prompt"
- Start designing!

---

## 📝 Prompt Template

```
You are "[NAME]", an expert [ROLE] powered by AI.

Your personality:
- [Trait 1]
- [Trait 2]
- [Trait 3]

Your role:
1. [Primary task]
2. [Secondary task]
3. [Tertiary task]

For [USE CASE], you need:
- [Required info 1]
- [Required info 2]
- [Required info 3]

Guidelines:
- [Guideline 1]
- [Guideline 2]
- [Guideline 3]

Start by [OPENING ACTION].
```

**Example**: See workshop guide Part 2

---

## ✅ Test Case Format

```json
{
  "test_id": 1,
  "scenario": "[Brief description]",
  "user_input": "[What user says]",
  "expected_action": "[What agent should do]",
  "pass_criteria": "[How to verify success]"
}
```

**5 Essential Test Cases**:
1. **Happy path**: All info provided
2. **Missing info**: Incomplete details
3. **Knowledge question**: "What is X?"
4. **Partial info**: Some details given
5. **Multi-turn**: Conversation over time

---

## 📚 FAQ Template

```
Category: [TOPIC]

Q: [Question]?
A: [Clear, concise answer in 1-2 sentences]

Q: [Question]?
A: [Answer with specific details or examples]
```

**Example FAQs**:
- What is [TERM]?
- How can I [ACTION]?
- Why is [SITUATION]?
- Do I need [FEATURE]?
- What's the difference between [X] and [Y]?

---

## 🎯 Your Workshop Tasks

### Part 2 (15 min): Design Agent Personality
- [ ] Open AI Studio
- [ ] Create system prompt using template
- [ ] Test with: "Hi, I need insurance"
- [ ] Refine until friendly and helpful
- [ ] Share with implementers

### Part 3 (20 min): Create Test Cases
- [ ] Write 5 test scenarios
- [ ] Include happy path, edge cases
- [ ] Define pass criteria
- [ ] Share with implementers
- [ ] Verify their code passes tests

### Part 4 (20 min): Write FAQs
- [ ] Create 10 insurance FAQs
- [ ] Cover: coverage types, discounts, general
- [ ] Keep answers clear and concise
- [ ] Share with implementers
- [ ] Test knowledge search

### Part 5 (15 min): Final Testing
- [ ] Test all 5 scenarios
- [ ] Ask FAQ questions
- [ ] Verify agent remembers context
- [ ] Document what works/doesn't
- [ ] Celebrate success!

---

## 🔧 AI Studio Tips

**Temperature Settings**:
- `0.0` = Consistent, same answer every time
- `0.5` = Balanced (recommended for agents)
- `1.0` = Creative, varied responses

**Testing Shortcuts**:
- Click "Run" to test prompt
- Use "Test your prompt" for variables
- Save prompts with descriptive names
- Share prompts via "Share" button

**Common Mistakes**:
- ❌ Prompt too vague → Be specific
- ❌ Too many instructions → Keep it simple
- ❌ No examples → Add few-shot examples
- ❌ Not testing → Always test before sharing

---

## 💬 Communication with Implementers

**What to share**:
1. **Prompts**: Read out loud or paste in chat
2. **Test cases**: Share the JSON format
3. **FAQs**: Paste the Q&A pairs
4. **Feedback**: "This works!" or "This needs fixing"

**When to speak up**:
- ✅ Agent personality doesn't match your design
- ✅ Test case fails
- ✅ FAQ answer is wrong
- ✅ Agent asks same question twice
- ✅ Response is unclear or unfriendly

---

## 📊 Success Metrics

**Your contributions**:
- ✅ System prompt that feels natural
- ✅ 5 comprehensive test cases
- ✅ 10 accurate FAQs
- ✅ Quality assurance feedback

**Agent should**:
- ✅ Sound friendly and professional
- ✅ Pass all your test cases
- ✅ Answer FAQs correctly
- ✅ Remember conversation context
- ✅ Explain clearly without jargon

---

## 🎉 You're Building AI!

**Remember**:
- You don't need to code to contribute
- Your design work is critical
- Prompt engineering is a real skill
- Testing ensures quality
- You're making the agent better!

---

## 📚 Quick Links

- **AI Studio**: https://aistudio.google.com/
- **Workshop Guide**: [Link to guide]
- **Community**: [Your community link]

---

**Questions? Ask the facilitator or an implementer!**

---

## Appendix: Sample Prompts

### Insurance Agent
```
You are "Alex", an expert insurance agent powered by AI.

Your personality:
- Friendly and professional
- Patient and helpful
- Explains complex terms simply

Your role:
1. Help customers get accurate quotes
2. Answer questions about coverage
3. Gather required information

For AUTO insurance, you need:
- Age, vehicle details, driving history

Guidelines:
- Ask 1-2 questions at a time
- Explain clearly when asked
- Calculate quote when ready

Start by greeting warmly.
```

### Customer Service Bot
```
You are "Sam", a helpful customer service agent.

Your personality:
- Empathetic and understanding
- Solution-oriented
- Never defensive

Your role:
1. Resolve customer issues
2. Provide product information
3. Escalate when needed

Guidelines:
- Acknowledge concerns first
- Offer solutions, not excuses
- Be concise but thorough

Start by asking how you can help.
```

---

**END OF QUICK REFERENCE CARD**
