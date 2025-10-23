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

  // Project Metrics API
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

  const fetchProjectTechnicalDebt = async (projectId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/project/${projectId}/technical-debt?period_days=${periodDays}`
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

  const fetchProjectBottlenecks = async (projectId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/project/${projectId}/bottlenecks?period_days=${periodDays}`
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

  const fetchProjectEmployeeCare = async (projectId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/project/${projectId}/employee-care?period_days=${periodDays}`
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
    // Project Metrics
    fetchProjectMetrics,
    fetchProjectTechnicalDebt,
    fetchProjectBottlenecks,
    fetchProjectEmployeeCare
  }
}
