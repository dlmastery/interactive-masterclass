import { useState } from "react";
import { Card, type Course, type RecordAttempt } from "./LabComponents.tsx";
export function Assessment(
  { course, record, jumpCore }: {
    course: Course;
    record: RecordAttempt;
    jumpCore: (n: number) => void;
  },
) {
  const [variant, setVariant] = useState(0),
    [index, setIndex] = useState(0),
    [answer, setAnswer] = useState(""),
    [reason, setReason] = useState(""),
    [guess, setGuess] = useState(false),
    [status, setStatus] = useState<"attempt" | "pass" | "stop">("attempt"),
    [explain, setExplain] = useState(false);
  const questions = course.examVariants[variant], q = questions[index];
  const reset = () => {
    setAnswer("");
    setReason("");
    setGuess(false);
    setStatus("attempt");
    setExplain(false);
  };
  return (
    <div className="assessment">
      <span className="phase">
        {explain
          ? "EXPLAINER"
          : status === "attempt"
          ? "EXAMINER · NO HINTS"
          : "CHECK RESULT"} · {q.level} · {index + 1} / {questions.length}
      </span>
      <h3>{q.prompt}</h3>
      <label>
        Answer<input
          aria-label="Exam answer"
          type="number"
          value={answer}
          disabled={status !== "attempt"}
          onChange={(e) => setAnswer(e.target.value)}
        />
      </label>
      <label>
        Reasoning<textarea
          aria-label="Exam reasoning"
          value={reason}
          disabled={status !== "attempt"}
          onChange={(e) => setReason(e.target.value)}
          placeholder="Write the steps you used. The number alone is not enough."
        />
      </label>
      <label className="check">
        <input
          type="checkbox"
          checked={guess}
          disabled={status !== "attempt"}
          onChange={(e) => setGuess(e.target.checked)}
        />I am guessing
      </label>
      {status === "attempt"
        ? (
          <button
            className="primary"
            disabled={!answer.trim() || !reason.trim()}
            onClick={() => {
              const correct =
                Math.abs(Number(answer) - q.answer) < q.tolerance && !guess;
              record({
                question: q.prompt,
                answer,
                reason,
                correct,
                guessed: guess,
              });
              setStatus(correct ? "pass" : "stop");
            }}
          >
            Submit without hints
          </button>
        )
        : status === "stop"
        ? (
          <Card>
            <strong>
              Assessment stopped{" "}
              {guess ? "on an admitted guess." : "at this calculation."}
            </strong>
            <p>No further exam questions until a fresh attempt.</p>
            <button onClick={() => jumpCore(q.route)}>
              Return to the relevant experiment
            </button>
            <button onClick={() => setExplain(true)}>
              Explain the stuck step
            </button>
            {explain && <p>{q.hint}</p>}
            <button
              onClick={() => {
                setVariant((variant + 1) % course.examVariants.length);
                setIndex(0);
                reset();
              }}
            >
              Start a fresh check with other numbers
            </button>
          </Card>
        )
        : (
          <Card>
            <strong>Numeric answer passes; reasoning saved for review.</strong>
            {index < questions.length - 1
              ? (
                <button
                  className="primary"
                  onClick={() => {
                    setIndex(index + 1);
                    reset();
                  }}
                >
                  Next question →
                </button>
              )
              : (
                <p>
                  All four numeric checks pass. Explain the
                  covariance-to-eigenvector argument in your own words to a
                  tutor before treating the topic as mastered.
                </p>
              )}
          </Card>
        )}
    </div>
  );
}
