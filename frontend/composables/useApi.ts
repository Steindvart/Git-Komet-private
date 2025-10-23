export const useApi = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Projects API
  const fetchProjects = async () => {
    try {
      const response = await fetch(`${apiBase}/projects`)
      return await response.json()
    } catch (error) {
      console.error('Error fetching projects:', error)
      return []
    }
  }

  const createProject = async (data: any) => {
    try {
      const response = await fetch(`${apiBase}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to create project')
      }
      return await response.json()
    } catch (error) {
      console.error('Error creating project:', error)
      throw error
    }
  }

  const deleteProject = async (id: number) => {
    try {
      const response = await fetch(`${apiBase}/projects/${id}`, {
        method: 'DELETE'
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to delete project')
      }
      return await response.json()
    } catch (error) {
      console.error('Error deleting project:', error)
      throw error
    }
  }

  // Repositories API
  const fetchRepositories = async (projectId: number) => {
    try {
      const response = await fetch(`${apiBase}/projects/${projectId}/repositories`)
      return await response.json()
    } catch (error) {
      console.error('Error fetching repositories:', error)
      return []
    }
  }

  // Project Metrics API (aggregated from repositories)
  const fetchProjectMetrics = async (projectId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/project/${projectId}/effectiveness?period_days=${periodDays}`
      )
      if (!response.ok) {
        throw new Error('Failed to fetch project metrics')
      }
      return await response.json()
    } catch (error) {
      console.error('Error fetching project metrics:', error)
      throw error
    }
  }

  // Repository Metrics API
  const fetchRepositoryMetrics = async (repositoryId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/repository/${repositoryId}/effectiveness?period_days=${periodDays}`
      )
      if (!response.ok) {
        throw new Error('Failed to fetch repository metrics')
      }
      return await response.json()
    } catch (error) {
      console.error('Error fetching repository metrics:', error)
      throw error
    }
  }

  const fetchRepositoryTechnicalDebt = async (repositoryId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/repository/${repositoryId}/technical-debt?period_days=${periodDays}`
      )
      if (!response.ok) {
        throw new Error('Failed to fetch technical debt')
      }
      return await response.json()
    } catch (error) {
      console.error('Error fetching technical debt:', error)
      throw error
    }
  }

  const fetchRepositoryBottlenecks = async (repositoryId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/repository/${repositoryId}/bottlenecks?period_days=${periodDays}`
      )
      if (!response.ok) {
        throw new Error('Failed to fetch bottlenecks')
      }
      return await response.json()
    } catch (error) {
      console.error('Error fetching bottlenecks:', error)
      throw error
    }
  }

  const fetchRepositoryEmployeeCare = async (repositoryId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/repository/${repositoryId}/employee-care?period_days=${periodDays}`
      )
      if (!response.ok) {
        throw new Error('Failed to fetch employee care metrics')
      }
      return await response.json()
    } catch (error) {
      console.error('Error fetching employee care metrics:', error)
      throw error
    }
  }

  return {
    // Projects
    fetchProjects,
    createProject,
    deleteProject,
    // Repositories
    fetchRepositories,
    // Project Metrics (aggregated)
    fetchProjectMetrics,
    // Repository Metrics
    fetchRepositoryMetrics,
    fetchRepositoryTechnicalDebt,
    fetchRepositoryBottlenecks,
    fetchRepositoryEmployeeCare
  }
}
