import React from 'react';
import { Car, Home, ArrowRight } from 'lucide-react';

const InsuranceTypeSelector = ({ onSelect }) => {
    return (
        <div className="mx-auto max-w-4xl px-4 py-16 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-primary">What type of insurance do you need?</h2>
                <p className="mt-4 text-xl text-secondary">Select the coverage type to get started.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Auto Insurance Option */}
                <button
                    onClick={() => onSelect('auto')}
                    className="group relative flex flex-col items-center p-8 bg-white rounded-2xl shadow-lg border-2 border-transparent hover:border-accent hover:shadow-xl transition-all duration-200"
                >
                    <div className="h-16 w-16 rounded-full bg-blue-50 flex items-center justify-center mb-6 group-hover:bg-blue-100 transition-colors">
                        <Car className="h-8 w-8 text-accent" />
                    </div>
                    <h3 className="text-xl font-bold text-primary mb-2">Auto Insurance</h3>
                    <p className="text-secondary mb-6 text-center">
                        Get coverage for your car, truck, or motorcycle.
                    </p>
                    <div className="mt-auto flex items-center text-accent font-medium group-hover:translate-x-1 transition-transform">
                        Get Auto Quote <ArrowRight className="ml-2 h-4 w-4" />
                    </div>
                </button>

                {/* Home Insurance Option */}
                <button
                    onClick={() => onSelect('home')}
                    className="group relative flex flex-col items-center p-8 bg-white rounded-2xl shadow-lg border-2 border-transparent hover:border-green-500 hover:shadow-xl transition-all duration-200"
                >
                    <div className="h-16 w-16 rounded-full bg-green-50 flex items-center justify-center mb-6 group-hover:bg-green-100 transition-colors">
                        <Home className="h-8 w-8 text-green-600" />
                    </div>
                    <h3 className="text-xl font-bold text-primary mb-2">Home Insurance</h3>
                    <p className="text-secondary mb-6 text-center">
                        Protect your home and personal belongings.
                    </p>
                    <div className="mt-auto flex items-center text-green-600 font-medium group-hover:translate-x-1 transition-transform">
                        Get Home Quote <ArrowRight className="ml-2 h-4 w-4" />
                    </div>
                </button>
            </div>
        </div>
    );
};

export default InsuranceTypeSelector;
