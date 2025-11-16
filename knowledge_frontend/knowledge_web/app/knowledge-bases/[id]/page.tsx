'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { KnowledgeBaseDetail } from '@/components/knowledge-base/detail'

export default function DetailPage() {
  const params = useParams()
  const kbId = params.id as string

  return (
    <div className="min-h-screen bg-gray-50">
      <KnowledgeBaseDetail kbId={kbId} />
    </div>
  )
}

