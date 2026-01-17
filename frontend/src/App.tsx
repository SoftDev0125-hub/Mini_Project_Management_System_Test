import React from 'react'
import { ApolloProvider } from '@apollo/client'
import { apolloClient } from './apollo/client'
import ProjectDashboard from './components/ProjectDashboard'

export default function App() {
  return (
    <ApolloProvider client={apolloClient}>
      <div className="min-h-screen p-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-semibold mb-4">Mini Project Management</h1>
          <ProjectDashboard />
        </div>
      </div>
    </ApolloProvider>
  )
}
