'use client'

import { Info } from 'lucide-react'

interface ChunkingConfigProps {
  chunkSize: number
  chunkOverlap: number
  onChunkSizeChange: (size: number) => void
  onChunkOverlapChange: (overlap: number) => void
}

export function ChunkingConfig({
  chunkSize,
  chunkOverlap,
  onChunkSizeChange,
  onChunkOverlapChange,
}: ChunkingConfigProps) {
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
      <div className="flex items-start gap-3 mb-6">
        <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div>
          <h3 className="font-semibold text-blue-900 mb-1">分块设置</h3>
          <p className="text-sm text-blue-800">
            配置文档如何分割成块以提高检索性能。
          </p>
        </div>
      </div>

      <div className="space-y-6">
        {/* Chunk Size */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            分块大小
          </label>
          <div className="flex items-center gap-4">
            <input
              type="range"
              min="256"
              max="2048"
              step="256"
              value={chunkSize}
              onChange={(e) => onChunkSizeChange(Number(e.target.value))}
              className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <div className="w-20 px-3 py-2 border border-gray-300 rounded-lg text-center font-medium text-gray-900">
              {chunkSize}
            </div>
          </div>
          <p className="text-xs text-gray-600 mt-2">
            较大的分块保留更多上下文但可能降低精度。推荐：512-1024
          </p>
        </div>

        {/* Chunk Overlap */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            分块重叠
          </label>
          <div className="flex items-center gap-4">
            <input
              type="range"
              min="0"
              max={Math.min(chunkSize - 1, 512)}
              step="50"
              value={chunkOverlap}
              onChange={(e) => onChunkOverlapChange(Number(e.target.value))}
              className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <div className="w-20 px-3 py-2 border border-gray-300 rounded-lg text-center font-medium text-gray-900">
              {chunkOverlap}
            </div>
          </div>
          <p className="text-xs text-gray-600 mt-2">
            重叠有助于保持分块之间的上下文。推荐：分块大小的 10-20%
          </p>
        </div>

        {/* Preview */}
        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <h4 className="font-medium text-gray-900 mb-3">预览</h4>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">分块大小:</span>
              <span className="font-medium text-gray-900">{chunkSize} 字符</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">重叠:</span>
              <span className="font-medium text-gray-900">
                {chunkOverlap} 字符 ({((chunkOverlap / chunkSize) * 100).toFixed(1)}%)
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">有效步长:</span>
              <span className="font-medium text-gray-900">
                {chunkSize - chunkOverlap} 字符
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

