'use client'

import { useState } from 'react'
import { CreateKnowledgeBase } from '@/components/knowledge-base/create'

export default function CreatePage() {
  const [step, setStep] = useState<'upload' | 'config' | 'complete'>('upload')
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [kbData, setKbData] = useState<any>(null)

  const handleFilesUploaded = (files: File[]) => {
    setUploadedFiles(files)
    setStep('config')
  }

  const handleConfigComplete = (data: any) => {
    setKbData(data)
    setStep('complete')
  }

  const handleReset = () => {
    setStep('upload')
    setUploadedFiles([])
    setKbData(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <CreateKnowledgeBase
          step={step}
          uploadedFiles={uploadedFiles}
          kbData={kbData}
          onFilesUploaded={handleFilesUploaded}
          onConfigComplete={handleConfigComplete}
          onReset={handleReset}
          onStepChange={setStep}
        />
      </div>
    </div>
  )
}

