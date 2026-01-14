import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import axios from 'axios'
import App from './App'

// Mock Axios
vi.mock('axios')
const mockedAxios = axios as any

describe('BrandGuardian UI', () => {

    it('renders the main dashboard correctly', () => {
        render(<App />)
        expect(screen.getByText('BrandGuardian')).toBeInTheDocument()
        expect(screen.getByText('Content Generator')).toBeInTheDocument()
        expect(screen.getByText('Visual Validator')).toBeInTheDocument()
    })

    it('switches tabs correctly', () => {
        render(<App />)

        // Click Visual Validator Tab
        fireEvent.click(screen.getByText('Visual Validator'))
        expect(screen.getByText('Visual Compliance Check')).toBeInTheDocument()

        // Click back to Text
        fireEvent.click(screen.getByText('Content Generator'))
        expect(screen.getByText('Briefing')).toBeInTheDocument()
    })

    it('handles content generation flow', async () => {
        // Setup Mock Response
        mockedAxios.post.mockResolvedValueOnce({
            data: {
                content: "Generated Vaisala Draft",
                brand_score: 90,
                reasoning: "Good job",
                used_references: ["Ref 1"]
            }
        })

        render(<App />)

        // Fill inputs
        const topicInput = screen.getByPlaceholderText(/e.g. Launch of new/i)
        fireEvent.change(topicInput, { target: { value: 'New Sensor' } })

        // Click Generate
        const btn = screen.getByText('Generate Draft')
        fireEvent.click(btn)

        // Wait for result
        await waitFor(() => {
            expect(screen.getByText('Generated Vaisala Draft')).toBeInTheDocument()
            expect(screen.getByText('90')).toBeInTheDocument()
        })
    })
})