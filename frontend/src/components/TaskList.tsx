import React from 'react'

interface Task {
  id: string
  title: string
  description?: string
  status: string
}

export default function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <div className="mt-4">
      {tasks.map((t) => (
        <div key={t.id} className="p-2 bg-white rounded mb-2">
          <div className="flex justify-between">
            <div>
              <div className="font-medium">{t.title}</div>
              <div className="text-sm text-slate-600">{t.description}</div>
            </div>
            <div className="text-sm">{t.status}</div>
          </div>
        </div>
      ))}
    </div>
  )
}
