import React, { useState } from 'react';
import { ArrowRight, User, MapPin, Car, Shield } from 'lucide-react';

const AutoInsuranceForm = ({ onSubmit, isLoading }) => {
    const [formData, setFormData] = useState({
        // Personal Info
        name: '',
        age: '',
        zip_code: '',

        // Vehicle Info
        vehicle_year: '',
        vehicle_make: '',
        vehicle_model: '',

        // Coverage Options
        liability_limit: '100000/300000',
        collision: true,
        comprehensive: true,
        deductible: '500',

        // Driver History
        years_licensed: '',
        accidents_3years: '0',
        violations_3years: '0',
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ ...formData, insurance_type: 'auto' });
    };

    return (
        <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
                <div className="px-6 py-8 sm:p-10 bg-slate-50 border-b border-slate-100">
                    <h3 className="text-2xl font-bold text-primary text-center">
                        Auto Insurance Quote
                    </h3>
                    <p className="mt-2 text-secondary text-center">
                        Tell us about yourself and your vehicle
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="px-6 py-8 sm:p-10 space-y-8">
                    {/* Personal Information */}
                    <div>
                        <h4 className="text-lg font-semibold text-primary mb-4 flex items-center">
                            <User className="h-5 w-5 mr-2 text-accent" />
                            Personal Information
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="name" className="block text-sm font-medium text-secondary mb-1">
                                    Full Name
                                </label>
                                <input
                                    type="text"
                                    name="name"
                                    id="name"
                                    required
                                    className="block w-full rounded-md border-slate-300 focus:border-accent focus:ring-accent sm:text-sm py-3 border"
                                    placeholder="John Doe"
                                    value={formData.name}
                                    onChange={handleChange}
                                />
                            </div>
                            <div>
                                <label htmlFor="age" className="block text-sm font-medium text-secondary mb-1">
                                    Age
                                </label>
                                <input
                                    type="number"
                                    name="age"
                                    id="age"
                                    required
                                    min="16"
                                    max="100"
                                    className="block w-full rounded-md border-slate-300 focus:border-accent focus:ring-accent sm:text-sm py-3 border"
                                    placeholder="30"
                                    value={formData.age}
                                    onChange={handleChange}
                                />
                            </div>
                            <div>
                                <label htmlFor="zip_code" className="block text-sm font-medium text-secondary mb-1">
                                    Zip Code
                                </label>
                                <input
                                    type="text"
                                    name="zip_code"
                                    id="zip_code"
                                    required
                                    pattern="[0-9]{5}"
                                    className="block w-full rounded-md border-slate-300 focus:border-accent focus:ring-accent sm:text-sm py-3 border"
                                    placeholder="10001"
                                    value={formData.zip_code}
                                    onChange={handleChange}
                                />
                            </div>
                            <div>
                                <label htmlFor="years_licensed" className="block text-sm font-medium text-secondary mb-1">
                                    Years Licensed
                                </label>
                                <input
                                    type="number"
                                    name="years_licensed"
                                    id="years_licensed"
                                    required
                                    min="0"
                                    max="80"
                                    className="block w-full rounded-md border-slate-300 focus:border-accent focus:ring-accent sm:text-sm py-3 border"
                                    placeholder="10"
                                    value={formData.years_licensed}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Vehicle Information */}
                    <div>
                        <h4 className="text-lg font-semibold text-primary mb-4 flex items-center">
                            <Car className="h-5 w-5 mr-2 text-accent" />
                            Vehicle Information
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div>
                                <label htmlFor="vehicle_year" className="block text-sm font-medium text-secondary mb-1">
                                    Year
                                </label>
                                <input
                                    type="number"
                                    name="vehicle_year"
                                    id="vehicle_year"
                                    required
                                    min="1980"
                                    max={new Date().getFullYear() + 1}
                                    className="block w-full rounded-md border-slate-300 focus:border-accent focus:ring-accent sm:text-sm py-3 border"
                                    placeholder="2020"
                                    value={formData.vehicle_year}
                                    onChange={handleChange}
                                />
                            </div>
                            <div>
                                <label htmlFor="vehicle_make" className="block text-sm font-medium text-secondary mb-1">
                                    Make
                                </label>
                                <input
                                    type="text"
                                    name="vehicle_make"
                                    id="vehicle_make"
                                    required
                                    className="block w-full rounded-md border-slate-300 focus:border-accent focus:ring-accent sm:text-sm py-3 border"
                                    placeholder="Toyota"
                                    value={formData.vehicle_make}
                                    onChange={handleChange}
                                />
                            </div>
                            <div>
                                <label htmlFor="vehicle_model" className="block text-sm font-medium text-secondary mb-1">
                                    Model
                                </label>
                                <input
                                    type="text"
                                    name="vehicle_model"
                                    id="vehicle_model"
                                    required
                                    className="block w-full rounded-md border-slate-300 focus:border-accent focus:ring-accent sm:text-sm py-3 border"
                                    placeholder="Camry"
                                    value={formData.vehicle_model}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Coverage Options */}
                    <div>
                        <h4 className="text-lg font-semibold text-primary mb-4 flex items-center">
                            <Shield className="h-5 w-5 mr-2 text-accent" />
                            Coverage Options
                        </h4>
                        <div className="space-y-4">
                            <div>
                                <label htmlFor="liability_limit" className="block text-sm font-medium text-secondary mb-1">
                                    Liability Limit
                                </label>
                                <select
                                    name="liability_limit"
                                    id="liability_limit"
                                    className="block w-full rounded-md border-slate-300 focus:border-accent focus:ring-accent sm:text-sm py-3 border bg-white"
                                    value={formData.liability_limit}
                                    onChange={handleChange}
                                >
                                    <option value="50000/100000">$50,000/$100,000</option>
                                    <option value="100000/300000">$100,000/$300,000</option>
                                    <option value="250000/500000">$250,000/$500,000</option>
                                    <option value="500000/1000000">$500,000/$1,000,000</option>
                                </select>
                            </div>

                            <div className="flex items-center space-x-6">
                                <label className="flex items-center">
                                    <input
                                        type="checkbox"
                                        name="collision"
                                        checked={formData.collision}
                                        onChange={handleChange}
                                        className="h-4 w-4 text-accent focus:ring-accent border-slate-300 rounded"
                                    />
                                    <span className="ml-2 text-sm text-secondary">Collision Coverage</span>
                                </label>
                                <label className="flex items-center">
                                    <input
                                        type="checkbox"
                                        name="comprehensive"
                                        checked={formData.comprehensive}
                                        onChange={handleChange}
                                        className="h-4 w-4 text-accent focus:ring-accent border-slate-300 rounded"
                                    />
                                    <span className="ml-2 text-sm text-secondary">Comprehensive Coverage</span>
                                </label>
                            </div>

                            <div>
                                <label htmlFor="deductible" className="block text-sm font-medium text-secondary mb-1">
                                    Deductible
                                </label>
                                <select
                                    name="deductible"
                                    id="deductible"
                                    className="block w-full rounded-md border-slate-300 focus:border-accent focus:ring-accent sm:text-sm py-3 border bg-white"
                                    value={formData.deductible}
                                    onChange={handleChange}
                                >
                                    <option value="250">$250</option>
                                    <option value="500">$500</option>
                                    <option value="1000">$1,000</option>
                                    <option value="2500">$2,500</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* Driver History */}
                    <div>
                        <h4 className="text-lg font-semibold text-primary mb-4">
                            Driver History (Last 3 Years)
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="accidents_3years" className="block text-sm font-medium text-secondary mb-1">
                                    Accidents
                                </label>
                                <select
                                    name="accidents_3years"
                                    id="accidents_3years"
                                    className="block w-full rounded-md border-slate-300 focus:border-accent focus:ring-accent sm:text-sm py-3 border bg-white"
                                    value={formData.accidents_3years}
                                    onChange={handleChange}
                                >
                                    <option value="0">0</option>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3+">3+</option>
                                </select>
                            </div>
                            <div>
                                <label htmlFor="violations_3years" className="block text-sm font-medium text-secondary mb-1">
                                    Violations
                                </label>
                                <select
                                    name="violations_3years"
                                    id="violations_3years"
                                    className="block w-full rounded-md border-slate-300 focus:border-accent focus:ring-accent sm:text-sm py-3 border bg-white"
                                    value={formData.violations_3years}
                                    onChange={handleChange}
                                >
                                    <option value="0">0</option>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3+">3+</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div className="pt-4">
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            {isLoading ? (
                                <span className="flex items-center">
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Calculating...
                                </span>
                            ) : (
                                <>
                                    Calculate Premium <ArrowRight className="ml-2 h-4 w-4" />
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default AutoInsuranceForm;
