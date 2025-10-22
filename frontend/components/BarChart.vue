<template>
  <div class="chart-container">
    <Bar 
      v-if="chartData"
      :data="chartData" 
      :options="chartOptions"
    />
  </div>
</template>

<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

interface Props {
  data: {
    labels: string[]
    values: number[]
  }
  title?: string
}

const props = defineProps<Props>()

const chartData = computed(() => {
  if (!props.data || !props.data.labels || !props.data.values) return null
  
  return {
    labels: props.data.labels,
    datasets: [
      {
        label: 'Часы',
        backgroundColor: '#3b82f6',
        borderColor: '#2563eb',
        borderWidth: 1,
        data: props.data.values
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    title: {
      display: !!props.title,
      text: props.title || ''
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Часы'
      }
    }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
</style>
