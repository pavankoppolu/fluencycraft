module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,OPTIONS,PATCH,DELETE,POST,PUT");
  res.setHeader("Access-Control-Allow-Headers", "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method Not Allowed. Use POST." });
  }

  try {
    const { answers, answerKey, learnerName } = req.body || {};
    if (!answers || !answerKey) {
      return res.status(400).json({ error: "Invalid payload. 'answers' and 'answerKey' are required." });
    }

    let score = 0;
    const total = Object.keys(answerKey).length;
    const breakdown = {};

    for (const key in answerKey) {
      const userAns = answers[key];
      const correctAns = answerKey[key].ans || answerKey[key];
      const isCorrect = userAns === correctAns;

      if (isCorrect) score++;

      breakdown[key] = {
        userAnswer: userAns || null,
        correctAnswer: correctAns,
        isCorrect,
        explanation: answerKey[key].exp || "Explanation unavailable."
      };
    }

    const percentage = Math.round((score / total) * 100);

    return res.status(200).json({
      status: "success",
      learnerName: learnerName || "Learner",
      score,
      total,
      percentage,
      breakdown,
      evaluatedAt: new Date().toISOString()
    });
  } catch (err) {
    return res.status(500).json({ error: err.message || "Internal server error during evaluation." });
  }
};
