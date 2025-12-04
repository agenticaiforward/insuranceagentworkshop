import React, { useState } from 'react';
import { ArrowRight, User, MapPin, Home as HomeIcon, Shield } from 'lucide-react';

const HomeInsuranceForm = ({ onSubmit, isLoading }) => {
    const [formData, setFormData] = useState({
        // Personal Info
        name: '',
        zip_code: '',

        // Property Info
        address: '',
        year_built: '',
        square_footage: '',
        stories: '1',

        // Construction
        construction_type: 'frame',
        roof_type: 'asphalt_shingle',

        // Coverage
        dwelling_coverage: '250000',
        personal_property: '100000',
        liability: '300000',

        // Features
        security_system: false,
        fire_alarm: false,
        has_pool: false,
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
        onSubmit({ ...formData, insurance_type: 'home' });
    };

    return (
        <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
                <div className="px-6 py-8 sm:p-10 bg-slate-50 border-b border-slate-100">
                    <h3 className="text-2xl font-bold text-primary text-center">
                        Home Insurance Quote
                    </h3>
                    <p className="mt-2 text-secondary text-center">
                        Tell us about your property
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="px-6 py-8 sm:p-10 space-y-8">
                    {/* Personal Information */}
                    <div>
                        <h4 className="text-lg font-semibold text-primary mb-4 flex items-center">
                            <User className="h-5 w-5 mr-2 text-green-600" />
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
                                    className="block w-full rounded-md border-slate-300 focus:border-green-500 focus:ring-green-500 sm:text-sm py-3 border"
                                    placeholder="John Doe"
                                    value={formData.name}
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
                                    className="block w-full rounded-md border-slate-300 focus:border-green-500 focus:ring-green-500 sm:text-sm py-3 border"
                                    placeholder="10001"
                                    value={formData.zip_code}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Property Information */}
                    <div>
                        <h4 className="text-lg font-semibold text-primary mb-4 flex items-center">
                            <HomeIcon className="h-5 w-5 mr-2 text-green-600" />
                            Property Information
                        </h4>
                        <div className="space-y-4">
                            <div>
                                <label htmlFor="address" className="block text-sm font-medium text-secondary mb-1">
                                    Property Address
                                </label>
                                <input
                                    type="text"
                                    name="address"
                                    id="address"
                                    required
                                    className="block w-full rounded-md border-slate-300 focus:border-green-500 focus:ring-green-500 sm:text-sm py-3 border"
                                    placeholder="123 Main St"
                                    value={formData.address}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div>
                                    <label htmlFor="year_built" className="block text-sm font-medium text-secondary mb-1">
                                        Year Built
                                    </label>
                                    <input
                                        type="number"
                                        name="year_built"
                                        id="year_built"
                                        required
                                        min="1800"
                                        max={new Date().getFullYear()}
                                        className="block w-full rounded-md border-slate-300 focus:border-green-500 focus:ring-green-500 sm:text-sm py-3 border"
                                        placeholder="2000"
                                        value={formData.year_built}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div>
                                    <label htmlFor="square_footage" className="block text-sm font-medium text-secondary mb-1">
                                        Square Footage
                                    </label>
                                    <input
                                        type="number"
                                        name="square_footage"
                                        id="square_footage"
                                        required
                                        min="500"
                                        max="20000"
                                        className="block w-full rounded-md border-slate-300 focus:border-green-500 focus:ring-green-500 sm:text-sm py-3 border"
                                        placeholder="2000"
                                        value={formData.square_footage}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div>
                                    <label htmlFor="stories" className="block text-sm font-medium text-secondary mb-1">
                                        Stories
                                    </label>
                                    <select
                                        name="stories"
                                        id="stories"
                                        className="block w-full rounded-md border-slate-300 focus:border-green-500 focus:ring-green-500 sm:text-sm py-3 border bg-white"
                                        value={formData.stories}
                                        onChange={handleChange}
                                    >
                                        <option value="1">1 Story</option>
                                        <option value="2">2 Stories</option>
                                        <option value="3">3+ Stories</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Construction Details */}
                    <div>
                        <h4 className="text-lg font-semibold text-primary mb-4">
                            Construction Details
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="construction_type" className="block text-sm font-medium text-secondary mb-1">
                                    Construction Type
                                </label>
                                <select
                                    name="construction_type"
                                    id="construction_type"
                                    className="block w-full rounded-md border-slate-300 focus:border-green-500 focus:ring-green-500 sm:text-sm py-3 border bg-white"
                                    value={formData.construction_type}
                                    onChange={handleChange}
                                >
                                    <option value="frame">Frame/Wood</option>
                                    <option value="brick">Brick</option>
                                    <option value="stone">Stone</option>
                                    <option value="concrete">Concrete</option>
                                </select>
                            </div>
                            <div>
                                <label htmlFor="roof_type" className="block text-sm font-medium text-secondary mb-1">
                                    Roof Type
                                </label>
                                <select
                                    name="roof_type"
                                    id="roof_type"
                                    className="block w-full rounded-md border-slate-300 focus:border-green-500 focus:ring-green-500 sm:text-sm py-3 border bg-white"
                                    value={formData.roof_type}
                                    onChange={handleChange}
                                >
                                    <option value="asphalt_shingle">Asphalt Shingle</option>
                                    <option value="metal">Metal</option>
                                    <option value="tile">Tile</option>
                                    <option value="slate">Slate</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* Coverage Options */}
                    <div>
                        <h4 className="text-lg font-semibold text-primary mb-4 flex items-center">
                            <Shield className="h-5 w-5 mr-2 text-green-600" />
                            Coverage Options
                        </h4>
                        <div className="space-y-4">
                            <div>
                                <label htmlFor="dwelling_coverage" className="block text-sm font-medium text-secondary mb-1">
                                    Dwelling Coverage
                                </label>
                                <select
                                    name="dwelling_coverage"
                                    id="dwelling_coverage"
                                    className="block w-full rounded-md border-slate-300 focus:border-green-500 focus:ring-green-500 sm:text-sm py-3 border bg-white"
                                    value={formData.dwelling_coverage}
                                    onChange={handleChange}
                                >
                                    <option value="150000">$150,000</option>
                                    <option value="250000">$250,000</option>
                                    <option value="350000">$350,000</option>
                                    <option value="500000">$500,000</option>
                                    <option value="750000">$750,000</option>
                                </select>
                            </div>
                            <div>
                                <label htmlFor="personal_property" className="block text-sm font-medium text-secondary mb-1">
                                    Personal Property Coverage
                                </label>
                                <select
                                    name="personal_property"
                                    id="personal_property"
                                    className="block w-full rounded-md border-slate-300 focus:border-green-500 focus:ring-green-500 sm:text-sm py-3 border bg-white"
                                    value={formData.personal_property}
                                    onChange={handleChange}
                                >
                                    <option value="50000">$50,000</option>
                                    <option value="75000">$75,000</option>
                                    <option value="100000">$100,000</option>
                                    <option value="150000">$150,000</option>
                                </select>
                            </div>
                            <div>
                                <label htmlFor="liability" className="block text-sm font-medium text-secondary mb-1">
                                    Liability Coverage
                                </label>
                                <select
                                    name="liability"
                                    id="liability"
                                    className="block w-full rounded-md border-slate-300 focus:border-green-500 focus:ring-green-500 sm:text-sm py-3 border bg-white"
                                    value={formData.liability}
                                    onChange={handleChange}
                                >
                                    <option value="100000">$100,000</option>
                                    <option value="300000">$300,000</option>
                                    <option value="500000">$500,000</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* Property Features */}
                    <div>
                        <h4 className="text-lg font-semibold text-primary mb-4">
                            Property Features
                        </h4>
                        <div className="space-y-3">
                            <label className="flex items-center">
                                <input
                                    type="checkbox"
                                    name="security_system"
                                    checked={formData.security_system}
                                    onChange={handleChange}
                                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-slate-300 rounded"
                                />
                                <span className="ml-2 text-sm text-secondary">Security System</span>
                            </label>
                            <label className="flex items-center">
                                <input
                                    type="checkbox"
                                    name="fire_alarm"
                                    checked={formData.fire_alarm}
                                    onChange={handleChange}
                                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-slate-300 rounded"
                                />
                                <span className="ml-2 text-sm text-secondary">Fire/Smoke Alarm</span>
                            </label>
                            <label className="flex items-center">
                                <input
                                    type="checkbox"
                                    name="has_pool"
                                    checked={formData.has_pool}
                                    onChange={handleChange}
                                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-slate-300 rounded"
                                />
                                <span className="ml-2 text-sm text-secondary">Swimming Pool</span>
                            </label>
                        </div>
                    </div>

                    <div className="pt-4">
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
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

export default HomeInsuranceForm;
