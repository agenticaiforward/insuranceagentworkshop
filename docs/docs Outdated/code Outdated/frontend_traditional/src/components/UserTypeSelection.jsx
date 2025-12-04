import React from 'react';
import { UserPlus, FileText, ArrowRight } from 'lucide-react';

const UserTypeSelection = ({ onSelect }) => {
    return (
        <div className="mx-auto max-w-4xl px-4 py-16 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-primary">How can we help you today?</h2>
                <p className="mt-4 text-xl text-secondary">Choose the option that best describes you.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* New Customer Option */}
                <button
                    onClick={() => onSelect('new')}
                    className="group relative flex flex-col items-center p-8 bg-white rounded-2xl shadow-lg border-2 border-transparent hover:border-accent hover:shadow-xl transition-all duration-200 text-left"
                >
                    <div className="h-16 w-16 rounded-full bg-blue-50 flex items-center justify-center mb-6 group-hover:bg-blue-100 transition-colors">
                        <UserPlus className="h-8 w-8 text-accent" />
                    </div>
                    <h3 className="text-xl font-bold text-primary mb-2">I'm a New Customer</h3>
                    <p className="text-secondary mb-6 text-center">
                        I need a new insurance quote tailored to my needs.
                    </p>
                    <div className="mt-auto flex items-center text-accent font-medium group-hover:translate-x-1 transition-transform">
                        Get Started <ArrowRight className="ml-2 h-4 w-4" />
                    </div>
                </button>

                {/* Existing Quote Option */}
                <button
                    onClick={() => onSelect('existing')}
                    className="group relative flex flex-col items-center p-8 bg-white rounded-2xl shadow-lg border-2 border-transparent hover:border-accent hover:shadow-xl transition-all duration-200 text-left"
                >
                    <div className="h-16 w-16 rounded-full bg-purple-50 flex items-center justify-center mb-6 group-hover:bg-purple-100 transition-colors">
                        <FileText className="h-8 w-8 text-purple-600" />
                    </div>
                    <h3 className="text-xl font-bold text-primary mb-2">I Have an Existing Quote</h3>
                    <p className="text-secondary mb-6 text-center">
                        Upload your current policy or quote to see if we can beat it.
                    </p>
                    <div className="mt-auto flex items-center text-purple-600 font-medium group-hover:translate-x-1 transition-transform">
                        Compare & Save <ArrowRight className="ml-2 h-4 w-4" />
                    </div>
                </button>
            </div>
        </div>
    );
};

export default UserTypeSelection;
