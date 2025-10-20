export const useApi = () => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  const fetchRepositories = async () => {
    try {
      const response = await fetch(`${apiBase}/repositories`)
      return await response.json()
    } catch (error) {
      console.error('Error fetching repositories:', error)
      return []
    }
  }

  const createRepository = async (data: any) => {
    try {
      const response = await fetch(`${apiBase}/repositories`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      return await response.json()
    } catch (error) {
      console.error('Error creating repository:', error)
      throw error
    }
  }

  const syncRepository = async (id: number) => {
    try {
      const response = await fetch(`${apiBase}/repositories/${id}/sync`, {
        method: 'POST'
      })
      return await response.json()
    } catch (error) {
      console.error('Error syncing repository:', error)
      throw error
    }
  }

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
      return await response.json()
    } catch (error) {
      console.error('Error creating team:', error)
      throw error
    }
  }

  const fetchTeamMetrics = async (teamId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/team/${teamId}/effectiveness?period_days=${periodDays}`
      )
      return await response.json()
    } catch (error) {
      console.error('Error fetching team metrics:', error)
      throw error
    }
  }

  const fetchRepositoryMetrics = async (repoId: number, periodDays: number = 30) => {
    try {
      const response = await fetch(
        `${apiBase}/metrics/repository/${repoId}?period_days=${periodDays}`
      )
      return await response.json()
    } catch (error) {
      console.error('Error fetching repository metrics:', error)
      throw error
    }
  }

  return {
    fetchRepositories,
    createRepository,
    syncRepository,
    fetchTeams,
    createTeam,
    fetchTeamMetrics,
    fetchRepositoryMetrics
  }
}
