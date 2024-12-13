import React from "react";

const HomePage: React.FC = () => {
  return (
    <div>
      <section className="h-lvh w-full bg-gradient-to-tr from-cyan-50 to-teal-200 to-indigo-600 py-12">
        <div className="container mx-auto text-center">
          <h3 className="text-3xl text-teal-800 font-semibold mb-8">
            Why Choose This?
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 p-2">
            <div className="p-6 bg-white shadow-lg rounded-lg">
              <h4 className="text-xl font-bold text-teal-700 mb-4">
                Track Expenses
              </h4>
              <p className="text-gray-700">
                Easily track and categorize your health expenses in one place.
              </p>
            </div>
            <div className="p-6 bg-white shadow-lg rounded-lg">
              <h4 className="text-xl font-bold text-teal-700 mb-4">
                Set Budget Goals
              </h4>
              <p className="text-gray-700">
                Set and monitor your budget goals to stay financially healthy.
              </p>
            </div>
            <div className="p-6 bg-white shadow-lg rounded-lg">
              <h4 className="text-xl font-bold text-teal-700 mb-4">
                Detailed Reports
              </h4>
              <p className="text-gray-700">
                Get comprehensive insights and reports for better
                decision-making.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
