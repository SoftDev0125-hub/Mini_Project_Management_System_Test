import React, { useState } from 'react'
import { gql, useQuery, useMutation } from '@apollo/client'

const PROJECTS_BY_ORG = gql`
  query ProjectsByOrg($orgSlug: String!) {
    projectsByOrg: projectsByOrg(orgSlug: $orgSlug) {
      id
      name
      description
      status
      taskCount
      completedTasks
    }
  }
`

const CREATE_PROJECT = gql`
  mutation CreateProject($orgSlug: String!, $name: String!, $description: String) {
    createProject(orgSlug: $orgSlug, name: $name, description: $description) {
      project { id name description status }
    }
  }
`

interface Project {
  id: string
  name: string
  description?: string
  status: string
  taskCount?: number
  completedTasks?: number
}

export default function ProjectDashboard() {
  const ORG_SLUG = 'demo'
  const { data, loading, error } = useQuery(PROJECTS_BY_ORG, { variables: { orgSlug: ORG_SLUG } })
  const [createProject] = useMutation(CREATE_PROJECT, {
    refetchQueries: [{ query: PROJECTS_BY_ORG, variables: { orgSlug: ORG_SLUG } }],
  })
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')

  if (loading) return <div>Loading projects...</div>
  if (error) return <div className="text-red-600">Error loading projects</div>

  const projects: Project[] = data?.projectsByOrg ?? []

  return (
    <div>
      <div className="mb-6">
        <form
          onSubmit={async (e) => {
            e.preventDefault()
            if (!name) return
            await createProject({ variables: { orgSlug: ORG_SLUG, name, description } })
            setName('')
            setDescription('')
          }}
        >
          <div className="flex gap-2">
            <input className="flex-1 p-2 border rounded" placeholder="Project name" value={name} onChange={(e) => setName(e.target.value)} />
            <button className="px-4 py-2 bg-blue-600 text-white rounded">Create</button>
          </div>
          <div className="mt-2">
            <input className="w-full p-2 border rounded" placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
          </div>
        </form>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {projects.map((p) => (
          <div key={p.id} className="p-4 bg-white rounded shadow-sm">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="font-medium">{p.name}</h2>
                <p className="text-sm text-slate-600">{p.description}</p>
              </div>
              <div className="text-right">
                <div className="text-sm">Status: <strong>{p.status}</strong></div>
                <div className="text-sm">Tasks: {p.taskCount ?? 0} • Done: {p.completedTasks ?? 0}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
