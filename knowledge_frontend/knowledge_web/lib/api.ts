/**
 * API client for Knowledge Base Management System
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'

export interface KnowledgeBase {
  id: string
  name: string
  description?: string
  created_at: string
  updated_at: string
  document_count: number
}

export interface Document {
  id: string
  knowledge_base_id: string
  name: string
  file_type: string
  file_size: number
  character_count: number
  chunk_count: number
  recall_count: number
  status: 'processing' | 'completed' | 'failed'
  created_at: string
  updated_at: string
}

export interface RetrievalResult {
  chunk_id: string
  document_id: string
  document_name: string
  content: string
  similarity_score: number
  chunk_index: number
}

export interface RetrievalResponse {
  query: string
  results: RetrievalResult[]
  total_count: number
}

// Knowledge Base APIs
export async function createKnowledgeBase(name: string, description?: string): Promise<KnowledgeBase> {
  const response = await fetch(`${API_BASE_URL}/knowledge-bases`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, description }),
  })
  if (!response.ok) throw new Error('Failed to create knowledge base')
  return response.json()
}

export async function getKnowledgeBase(id: string): Promise<KnowledgeBase> {
  const response = await fetch(`${API_BASE_URL}/knowledge-bases/${id}`)
  if (!response.ok) throw new Error('Failed to get knowledge base')
  return response.json()
}

export async function listKnowledgeBases(): Promise<KnowledgeBase[]> {
  const response = await fetch(`${API_BASE_URL}/knowledge-bases`)
  if (!response.ok) throw new Error('Failed to list knowledge bases')
  return response.json()
}

export async function updateKnowledgeBase(id: string, name?: string, description?: string): Promise<KnowledgeBase> {
  const response = await fetch(`${API_BASE_URL}/knowledge-bases/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, description }),
  })
  if (!response.ok) throw new Error('Failed to update knowledge base')
  return response.json()
}

export async function deleteKnowledgeBase(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/knowledge-bases/${id}`, {
    method: 'DELETE',
  })
  if (!response.ok) throw new Error('Failed to delete knowledge base')
}

// Document APIs
export async function uploadDocuments(
  kbId: string,
  files: File[],
  chunkSize: number = 1024,
  chunkOverlap: number = 200
): Promise<{ documents: Document[]; count: number }> {
  const formData = new FormData()
  files.forEach(file => formData.append('files', file))
  formData.append('chunk_size', chunkSize.toString())
  formData.append('chunk_overlap', chunkOverlap.toString())

  const response = await fetch(`${API_BASE_URL}/documents/${kbId}/upload`, {
    method: 'POST',
    body: formData,
  })
  if (!response.ok) throw new Error('Failed to upload documents')
  return response.json()
}

export async function listDocuments(kbId: string): Promise<Document[]> {
  const response = await fetch(`${API_BASE_URL}/documents/${kbId}`)
  if (!response.ok) throw new Error('Failed to list documents')
  return response.json()
}

export async function deleteDocument(docId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/documents/${docId}`, {
    method: 'DELETE',
  })
  if (!response.ok) throw new Error('Failed to delete document')
}

// Retrieval APIs
export async function searchKnowledgeBase(
  kbId: string,
  query: string,
  topK: number = 5,
  retrievalType: 'vector' | 'hybrid' = 'vector'
): Promise<RetrievalResponse> {
  const response = await fetch(`${API_BASE_URL}/retrieval/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      knowledge_base_id: kbId,
      top_k: topK,
      retrieval_type: retrievalType,
    }),
  })
  if (!response.ok) throw new Error('Failed to search knowledge base')
  return response.json()
}

export async function previewChunks(
  kbId: string,
  docId: string,
  chunkSize: number = 1024,
  chunkOverlap: number = 200
): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/retrieval/preview-chunks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      kb_id: kbId,
      doc_id: docId,
      chunk_size: chunkSize,
      chunk_overlap: chunkOverlap,
    }),
  })
  if (!response.ok) throw new Error('Failed to preview chunks')
  return response.json()
}

