/**
 * Главный компонент wizard для примерки
 * Управляет навигацией между шагами и процессом генерации
 */

import React, { useState } from 'react';
import { Step1UserPhoto } from './Step1UserPhoto';
import { Step2ItemPhoto } from './Step2ItemPhoto';
import { Step3Zone } from './Step3Zone';
import { GenerationProgress } from './GenerationProgress';
import { FittingResult } from './FittingResult';
import { useFittingStore } from '../../store/fittingStore';
import toast from 'react-hot-toast';

type WizardStep = 'user_photo' | 'item_photo' | 'zone' | 'generating' | 'result';

export const FittingWizard: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<WizardStep>('user_photo');
  const { startGeneration } = useFittingStore();

  const handleGenerateClick = async () => {
    setCurrentStep('generating');

    try {
      await startGeneration();
      setCurrentStep('result');
    } catch (error: any) {
      toast.error(error.message || 'Ошибка генерации');
      // Остаёмся на шаге выбора зоны при ошибке
      setCurrentStep('zone');
    }
  };

  const handleRestart = () => {
    setCurrentStep('user_photo');
  };

  // Progress indicator
  const getStepNumber = (): number => {
    switch (currentStep) {
      case 'user_photo':
        return 1;
      case 'item_photo':
        return 2;
      case 'zone':
        return 3;
      case 'generating':
      case 'result':
        return 3;
      default:
        return 1;
    }
  };

  const totalSteps = 3;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Progress indicator */}
      {currentStep !== 'generating' && currentStep !== 'result' && (
        <div className="bg-white border-b border-gray-200 py-4 px-4">
          <div className="max-w-2xl mx-auto">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                Шаг {getStepNumber()} из {totalSteps}
              </span>
              <span className="text-xs text-gray-500">
                {Math.round((getStepNumber() / totalSteps) * 100)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${(getStepNumber() / totalSteps) * 100}%` }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Main content */}
      <div className="py-6">
        {currentStep === 'user_photo' && (
          <Step1UserPhoto onNext={() => setCurrentStep('item_photo')} />
        )}

        {currentStep === 'item_photo' && (
          <Step2ItemPhoto
            onNext={() => setCurrentStep('zone')}
            onBack={() => setCurrentStep('user_photo')}
          />
        )}

        {currentStep === 'zone' && (
          <Step3Zone
            onBack={() => setCurrentStep('item_photo')}
            onGenerate={handleGenerateClick}
          />
        )}

        {currentStep === 'generating' && <GenerationProgress />}

        {currentStep === 'result' && (
          <FittingResult onNewFitting={handleRestart} />
        )}
      </div>
    </div>
  );
};
