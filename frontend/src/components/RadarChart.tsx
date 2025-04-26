import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js';
import { RadarChartData } from '../Interface';


export const SocialStyleChart: React.FC<{ data: RadarChartData }> = ({ data }) => {
    const chartRef = useRef<HTMLCanvasElement>(null);
    
    useEffect(() => {
        if (data && chartRef.current) {
            const ctx = chartRef.current.getContext('2d');
            if (ctx) {
                new Chart(ctx, {
                    type: 'radar',
                    data: {
                        labels: data.labels,
                        datasets: [
                            {
                                label: 'Post-Coaching',
                                data: data.post_values,
                                backgroundColor:'transparent',
                                borderColor: 'rgba(255, 99, 132, 1)',
                                borderWidth: 2,
                            },
                        ]
                    },
                    options: {
                        scale: {
                            // gridLines: {
                            //     circular: true,
                            // },
                            ticks: {
                                showLabelBackdrop: false,
                                beginAtZero: true,
                                stepSize: 10,
                                min: 0,
                                max: data.post_values.length>0? data.post_values.reduce((a, b) => Math.max(a, b)) + 10 : 50,
                                fontSize: 14,
                                fontColor: 'black',
                                fontFamily: "'Noto Sans TC', sans-serif",
                                
                            },
                            pointLabels: {
                                fontColor: 'black',
                                fontSize: 14,
                                fontFamily: 'Noto Sans TC', 
                            }
                        },
                        legend: {
                            display: true,
                            position: 'top', // Position the legend at the top
                            align: 'start',  // Align the legend to the start (left)
                            labels: {
                                fontSize: 14, 
                                fontStyle: 'bold' 
                            }
                        }
                    }
                });
            }
        }
    }, [data]);

    return <canvas ref={chartRef} />;
};


export const ModelChart: React.FC<{ data: RadarChartData }> = ({ data }) => {
    const chartRef = useRef<HTMLCanvasElement>(null);


    useEffect(() => {
        if (data && chartRef.current) {
            const ctx = chartRef.current.getContext('2d');
            if (ctx) {
                new Chart(ctx, {
                    type: 'radar',
                    data: {
                        labels: data.labels,
                        datasets: [
                            {
                                label: 'Post-Coaching',
                                data: data.post_values,

                                backgroundColor:'transparent',
                                borderColor: 'rgba(255, 99, 132, 1)',
                                borderWidth: 2,
                            },
                            {
                                label: 'Pre-Coaching',
                                data: data.pre_values,
                                backgroundColor:'transparent',
                                borderColor: 'rgba(54, 162, 235, 1)',
                                borderWidth: 2
                            }
                        ]
                    },
                    options: {
                        scale: {
                            gridLines: {
                                circular: true,
                            },
                            ticks: {
                                showLabelBackdrop: false,
                                beginAtZero: true,
                                stepSize: 1,
                                min: 1,
                                max: 6,
                                fontSize: 14,
                                fontColor: 'black',
                                fontFamily: "'Noto Sans TC', sans-serif",
                                
                            },
                            pointLabels: {
                                fontColor: 'black',
                                fontSize: 14,
                                fontFamily: 'Noto Sans TC', 
                            }
                        },
                        legend: {
                            display: true,
                            position: 'top', // Position the legend at the top
                            align: 'start',  // Align the legend to the start (left)
                            labels: {
                                fontSize: 14, 
                                fontStyle: 'bold' 
                            }
                        }
                    }
                });
            }
        }
    }, [data]);

    return <canvas ref={chartRef} />;
};