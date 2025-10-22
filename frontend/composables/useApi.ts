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

  const generateMockData = async (projectId: number, teamId: number) => {
    try {
      const response = await fetch(`${apiBase}/projects/${projectId}/generate-mock-data?team_id=${teamId}`, {
        method: 'POST'
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to generate mock data')
      }
      return await response.json()
    } catch (error) {
      console.error('Error generating mock data:', error)
      throw error
    }
  }

  // Teams API
  const fetchTeams = async () => {
    try {
      const response = await fetch(`${apiBase}/teams`)
      return await response.json()
    } catch (error) {
      console.error('Error fetching teams:', error)
      return []
    }
  }

  const createTeam = async (data: any) => {
    try {
      const response = await fetch(`${apiBase}/teams`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to create team')
      }
      return await response.json()
    } catch (error) {
      console.error('Error creating team:', error)
      throw error
    }
  }

  const deleteTeam = async (id: number) => {
    try {
      const response = await fetch(`${apiBase}/teams/${id}`, {
        method: 'DELETE'
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to delete team')
      }
      return await response.json()
    } catch (error) {
      console.error('Error deleting team:', error)
      throw error
    }
  }

  const addTeamMember = async (data: any) => {
    try {
      const response = await fetch(`${apiBase}/teams/members`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to add team member')
      }
      return await response.json()
    } catch (error) {
      console.error('Error adding team member:', error)
      throw error
    }
  }

  // Metrics API
  const fetchTeamMetrics = async (teamId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/team/${teamId}/effectiveness?period_days=${periodDays}`
      )
      if (!response.ok) {
        throw new Error('Failed to fetch team metrics')
      }
      return await response.json()
    } catch (error) {
      console.error('Error fetching team metrics:', error)
      throw error
    }
  }

  const fetchTechnicalDebt = async (teamId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/team/${teamId}/technical-debt?period_days=${periodDays}`
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

  const fetchBottlenecks = async (teamId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/team/${teamId}/bottlenecks?period_days=${periodDays}`
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

  return {
    // Projects
    fetchProjects,
    createProject,
    deleteProject,
    generateMockData,
    // Teams
    fetchTeams,
    createTeam,
    deleteTeam,
    addTeamMember,
    // Metrics
    fetchTeamMetrics,
    fetchTechnicalDebt,
    fetchBottlenecks
  }
}
