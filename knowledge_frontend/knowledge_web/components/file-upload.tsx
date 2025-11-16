'use client'

import { useState, useRef } from 'react'
import { Upload, X, File } from 'lucide-react'
import { toast } from 'react-hot-toast'

interface FileUploadProps {
  onFilesSelected: (files: File[]) => void
}

const SUPPORTED_FORMATS = [
  'pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'txt', 'md', 'markdown',
  'html', 'htm', 'xml', 'ppt', 'pptx'
]
const MAX_FILE_SIZE = 15 * 1024 * 1024 // 15MB
const MAX_FILES = 5

export function FileUpload({ onFilesSelected }: FileUploadProps) {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const validateFiles = (files: FileList): File[] => {
    const validFiles: File[] = []
    const errors: string[] = []

    if (files.length + selectedFiles.length > MAX_FILES) {
      errors.push(`每批最多允许 ${MAX_FILES} 个文件`)
    }

    Array.from(files).forEach((file) => {
      const ext = file.name.split('.').pop()?.toLowerCase()
      
      if (!ext || !SUPPORTED_FORMATS.includes(ext)) {
        errors.push(`${file.name}: 不支持的格式`)
        return
      }

      if (file.size > MAX_FILE_SIZE) {
        errors.push(`${file.name}: 文件大小超过 15MB 限制`)
        return
      }

      validFiles.push(file)
    })

    errors.forEach(error => toast.error(error))
    return validFiles
  }

  const handleFileSelect = (files: FileList | null) => {
    if (!files) return

    const validFiles = validateFiles(files)
    if (validFiles.length > 0) {
      const newFiles = [...selectedFiles, ...validFiles]
      setSelectedFiles(newFiles)
      onFilesSelected(newFiles)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    handleFileSelect(e.dataTransfer.files)
  }

  const removeFile = (index: number) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index)
    setSelectedFiles(newFiles)
    onFilesSelected(newFiles)
  }

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          isDragging
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 bg-gray-50 hover:border-gray-400'
        }`}
      >
        <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-lg font-medium text-gray-900 mb-2">
          拖拽文件到此处
        </p>
        <p className="text-sm text-gray-600 mb-4">
          或点击选择文件
        </p>
        <button
          onClick={() => fileInputRef.current?.click()}
          className="inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          选择文件
        </button>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          onChange={(e) => handleFileSelect(e.target.files)}
          accept={SUPPORTED_FORMATS.map(f => `.${f}`).join(',')}
          className="hidden"
        />
        <p className="text-xs text-gray-500 mt-4">
          支持的格式: {SUPPORTED_FORMATS.join(', ')}
        </p>
        <p className="text-xs text-gray-500">
          最多 {MAX_FILES} 个文件，每个文件最大 {MAX_FILE_SIZE / 1024 / 1024}MB
        </p>
      </div>

      {/* File List */}
      {selectedFiles.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <h3 className="font-medium text-gray-900 mb-3">
            已选择文件 ({selectedFiles.length}/{MAX_FILES})
          </h3>
          <div className="space-y-2">
            {selectedFiles.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center gap-3 flex-1">
                  <File className="w-5 h-5 text-gray-400" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

