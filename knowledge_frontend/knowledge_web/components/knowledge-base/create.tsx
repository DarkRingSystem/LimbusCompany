'use client'

import { useState } from 'react'
import { ChevronRight, Check } from 'lucide-react'
import { FileUpload } from '@/components/file-upload'
import { ChunkingConfig } from '@/components/chunking-config'
import { createKnowledgeBase, uploadDocuments } from '@/lib/api'
import { toast } from 'react-hot-toast'
import Link from 'next/link'

interface CreateKnowledgeBaseProps {
  step: 'upload' | 'config' | 'complete'
  uploadedFiles: File[]
  kbData: any
  onFilesUploaded: (files: File[]) => void
  onConfigComplete: (data: any) => void
  onReset: () => void
  onStepChange: (step: 'upload' | 'config' | 'complete') => void
}

export function CreateKnowledgeBase({
  step,
  uploadedFiles,
  kbData,
  onFilesUploaded,
  onConfigComplete,
  onReset,
  onStepChange,
}: CreateKnowledgeBaseProps) {
  const [kbName, setKbName] = useState('')
  const [kbDescription, setKbDescription] = useState('')
  const [chunkSize, setChunkSize] = useState(1024)
  const [chunkOverlap, setChunkOverlap] = useState(200)
  const [isLoading, setIsLoading] = useState(false)

  const handleCreateKB = async () => {
    if (!kbName.trim()) {
      toast.error('请输入知识库名称')
      return
    }

    try {
      setIsLoading(true)
      const kb = await createKnowledgeBase(kbName, kbDescription)
      
      if (uploadedFiles.length > 0) {
        await uploadDocuments(kb.id, uploadedFiles, chunkSize, chunkOverlap)
      }

      onConfigComplete({
        id: kb.id,
        name: kb.name,
        description: kb.description,
        chunkSize,
        chunkOverlap,
      })
      toast.success('知识库创建成功')
    } catch (err) {
      const message = err instanceof Error ? err.message : '创建知识库失败'
      toast.error(message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div>
      {/* Step Indicator */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {['上传', '配置', '完成'].map((label, index) => (
            <div key={label} className="flex items-center flex-1">
              <div
                className={`flex items-center justify-center w-10 h-10 rounded-full font-semibold ${
                  index < ['upload', 'config', 'complete'].indexOf(step)
                    ? 'bg-green-500 text-white'
                    : index === ['upload', 'config', 'complete'].indexOf(step)
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                {index < ['upload', 'config', 'complete'].indexOf(step) ? (
                  <Check className="w-6 h-6" />
                ) : (
                  index + 1
                )}
              </div>
              <span className="ml-2 text-sm font-medium text-gray-700">{label}</span>
              {index < 2 && <ChevronRight className="w-5 h-5 text-gray-400 mx-2 flex-1" />}
            </div>
          ))}
        </div>
      </div>

      {/* Step Content */}
      <div className="bg-white rounded-lg shadow p-8">
        {step === 'upload' && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">上传文档</h2>
            <FileUpload onFilesSelected={onFilesUploaded} />
            <div className="mt-6 flex justify-end">
              <button
                onClick={() => onStepChange('config')}
                disabled={uploadedFiles.length === 0}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                下一步：配置
              </button>
            </div>
          </div>
        )}

        {step === 'config' && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">配置知识库</h2>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  知识库名称 *
                </label>
                <input
                  type="text"
                  value={kbName}
                  onChange={(e) => setKbName(e.target.value)}
                  placeholder="请输入知识库名称"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  描述
                </label>
                <textarea
                  value={kbDescription}
                  onChange={(e) => setKbDescription(e.target.value)}
                  placeholder="请输入知识库描述"
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <ChunkingConfig
                chunkSize={chunkSize}
                chunkOverlap={chunkOverlap}
                onChunkSizeChange={setChunkSize}
                onChunkOverlapChange={setChunkOverlap}
              />
            </div>

            <div className="mt-8 flex justify-between">
              <button
                onClick={() => onStepChange('upload')}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                返回
              </button>
              <button
                onClick={handleCreateKB}
                disabled={isLoading}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? '创建中...' : '创建知识库'}
              </button>
            </div>
          </div>
        )}

        {step === 'complete' && kbData && (
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <div className="flex items-center justify-center w-16 h-16 rounded-full bg-green-100">
                <Check className="w-8 h-8 text-green-600" />
              </div>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">知识库创建成功！</h2>
            <p className="text-gray-600 mb-6">
              您的知识库 "{kbData.name}" 已成功创建。
            </p>
            
            <div className="flex gap-4 justify-center">
              <Link
                href={`/knowledge-bases/${kbData.id}`}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                查看知识库
              </Link>
              <button
                onClick={onReset}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                创建另一个
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

