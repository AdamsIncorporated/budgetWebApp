import React from "react";

interface TutorialStepProps {
  stepNumber: number;
  title: string;
  description: string;
  imageUrl?: string;
}

const TutorialStep: React.FC<TutorialStepProps> = ({
  stepNumber,
  title,
  description,
  imageUrl,
}) => {
  return (
    <div className="tutorial-step">
      <h3 className="step-number">{stepNumber}.</h3>
      <h2 className="step-title">{title}</h2>
      <p className="step-description">{description}</p>
      {imageUrl && <img src={imageUrl} alt={title} />}
    </div>
  );
};

const TutorialPage: React.FC = () => {
  const tutorialSteps = [
    {
      stepNumber: 1,
      title: "Getting Started",
      description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
      imageUrl: "https://example.com/image1.jpg",
    },
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-teal-600">
        Welcome to the Tutorial
      </h1>

      <div className="space-y-8">
        <div className="bg-cyan-100 p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold text-teal-600">
            Step 1: Getting Started
          </h2>
          <p className="text-gray-700">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </p>
        </div>

        <button className="bg-teal-500 hover:bg-teal-600 text-white font-bold py-2 px-4 rounded">
          Next Step
        </button>
      </div>
    </div>
  );
};

export default TutorialPage;
