'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { KnowledgeBaseList } from '@/components/knowledge-base/list'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">知识库</h1>
            <p className="mt-2 text-gray-600">管理您的知识库和文档</p>
          </div>
          <Link
            href="/create"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
          >
            + 创建知识库
          </Link>
        </div>
        
        <KnowledgeBaseList />
      </div>
    </div>
  )
}

