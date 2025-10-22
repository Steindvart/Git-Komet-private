export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase || 'http://localhost:8001'

  const fetchProjects = async () => {
    try {
      const response = await $fetch(`${baseURL}/projects/`)
      return response
    } catch (error) {
      console.error('Error fetching projects:', error)
      throw error
    }
  }

  const fetchBottleneckAnalysis = async (projectId: number) => {
    try {
      const response = await $fetch(`${baseURL}/metrics/bottlenecks/${projectId}`)
      return response
    } catch (error) {
      console.error('Error fetching bottleneck analysis:', error)
      throw error
    }
  }

  const generateMockData = async () => {
    try {
      const response = await $fetch(`${baseURL}/mock/generate`, {
        method: 'POST'
      })
      return response
    } catch (error) {
      console.error('Error generating mock data:', error)
      throw error
    }
  }

  const clearMockData = async () => {
    try {
      const response = await $fetch(`${baseURL}/mock/clear`, {
        method: 'DELETE'
      })
      return response
    } catch (error) {
      console.error('Error clearing mock data:', error)
      throw error
    }
  }

  return {
    fetchProjects,
    fetchBottleneckAnalysis,
    generateMockData,
    clearMockData
  }
}
