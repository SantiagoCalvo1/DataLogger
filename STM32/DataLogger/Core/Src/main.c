/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define BUFFER_SIZE				10
#define ENVIAR_BUFFER 			'E'
#define CONFIGURAR				'C'
#define NADA 					'N'
#define ADQUIRIR 				'A'

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc1;

TIM_HandleTypeDef htim3;

UART_HandleTypeDef huart2;
DMA_HandleTypeDef hdma_usart2_tx;

/* USER CODE BEGIN PV */
uint8_t adc_buffer[BUFFER_SIZE];
uint16_t adc_index;
uint8_t error_buffer;
uint8_t rx_dato;
uint8_t tx_dato;
uint8_t flag_cambio;
uint8_t flag_actual;
/*
uint8_t enviar_buffer =	'E';
uint8_t configurar=	'C';
uint8_t nada= 'N';
uint8_t adquirir= 'A';
*/
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_ADC1_Init(void);
static void MX_TIM3_Init(void);
static void MX_USART2_UART_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_ADC1_Init();
  MX_TIM3_Init();
  MX_USART2_UART_Init();
  /* USER CODE BEGIN 2 */
  flag_cambio = 0;
  flag_actual = NADA;
  adc_index = 0;
  error_buffer = 0;

  // LLenar el buffer para pruebas
  for (uint16_t i=0; i<BUFFER_SIZE; i++){
	  adc_buffer[i] = i%255;
  }

  HAL_ADCEx_Calibration_Start(&hadc1);
  //HAL_ADC_Start_IT(&hadc1);
  //HAL_TIM_Base_Start(&htim3);
  HAL_UART_Receive_IT(&huart2, &rx_dato, 1);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
	  /*
	  if (flag_actual == NADA){
		  // Toggle solo para ubicar donde está
		  HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
		  HAL_Delay(200);
	  }
	  */
	  if (flag_cambio == 1){
		switch (flag_actual)
		{
		case ENVIAR_BUFFER:
			flag_actual = ENVIAR_BUFFER;
			HAL_UART_Transmit(&huart2, &flag_actual, 1, 1);
			// Detiene el TIM3 y por lo tento el ADC
			HAL_ADC_Stop_IT(&hadc1);
			HAL_TIM_Base_Stop(&htim3);
			// Verifica si hubo error por overflow en el adc_buffer
			if (error_buffer == 1){
				// Significa que el buffer hizo overflow y se sobreescribieron datos
				adc_buffer[0] = 0xFF;
				// El código 0xFF indica que hubo error. El ADC está mapeado de 0 a 254.
			}
			// Activa transmisión DMA del buffer
			HAL_UART_Transmit_DMA(&huart2, adc_buffer, BUFFER_SIZE);
			// En el callback del Tx se sale de este modo
			break;

		case CONFIGURAR:
			flag_actual = CONFIGURAR;
			// Completar
			break;

		case NADA:
			flag_actual = NADA;
			// Se frena al ADC
			HAL_ADC_Stop_IT(&hadc1);
			HAL_TIM_Base_Stop(&htim3);
			break;

		case ADQUIRIR:
			flag_actual = ADQUIRIR;
			// Se resetea index_adc
			adc_index = 0;
			// Se resetea el error del buffer
			error_buffer = 0;
			// Comienza el ADC IT (se renueva dentro de la misma rutina)
			HAL_ADC_Start_IT(&hadc1);
			// Comienza el TIM3 para disparar al ADC
			HAL_TIM_Base_Start(&htim3);
			break;

		default:
			HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
			flag_actual = 0;
		}
		// El flag tiene que dejar de estar en cambio de flag
		flag_cambio = 0;
		// Una vez hecho lo que habia que hacer, se activan Rx_IT
		// Y se confirma recepcion
		if ((flag_actual != ENVIAR_BUFFER) && (flag_actual != 0)){
			HAL_UART_Transmit(&huart2, &flag_actual, 1, 1);
			HAL_UART_Receive_IT(&huart2, &rx_dato, 1);
		}
		if (flag_actual == 0){
			flag_actual = NADA;
		}
	  }
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_ADC;
  PeriphClkInit.AdcClockSelection = RCC_ADCPCLK2_DIV2;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief ADC1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_ADC1_Init(void)
{

  /* USER CODE BEGIN ADC1_Init 0 */

  /* USER CODE END ADC1_Init 0 */

  ADC_ChannelConfTypeDef sConfig = {0};

  /* USER CODE BEGIN ADC1_Init 1 */

  /* USER CODE END ADC1_Init 1 */
  /** Common config
  */
  hadc1.Instance = ADC1;
  hadc1.Init.ScanConvMode = ADC_SCAN_DISABLE;
  hadc1.Init.ContinuousConvMode = DISABLE;
  hadc1.Init.DiscontinuousConvMode = DISABLE;
  hadc1.Init.ExternalTrigConv = ADC_EXTERNALTRIGCONV_T3_TRGO;
  hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc1.Init.NbrOfConversion = 1;
  if (HAL_ADC_Init(&hadc1) != HAL_OK)
  {
    Error_Handler();
  }
  /** Configure Regular Channel
  */
  sConfig.Channel = ADC_CHANNEL_0;
  sConfig.Rank = ADC_REGULAR_RANK_1;
  sConfig.SamplingTime = ADC_SAMPLETIME_239CYCLES_5;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN ADC1_Init 2 */

  /* USER CODE END ADC1_Init 2 */

}

/**
  * @brief TIM3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM3_Init(void)
{

  /* USER CODE BEGIN TIM3_Init 0 */

  /* USER CODE END TIM3_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM3_Init 1 */

  /* USER CODE END TIM3_Init 1 */
  htim3.Instance = TIM3;
  htim3.Init.Prescaler = 7999;
  htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim3.Init.Period = 999;
  htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim3, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_UPDATE;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_ENABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim3, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM3_Init 2 */

  /* USER CODE END TIM3_Init 2 */

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * Enable DMA controller clock
  */
static void MX_DMA_Init(void)
{

  /* DMA controller clock enable */
  __HAL_RCC_DMA1_CLK_ENABLE();

  /* DMA interrupt init */
  /* DMA1_Channel7_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Channel7_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA1_Channel7_IRQn);

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : LED_Pin */
  GPIO_InitStruct.Pin = LED_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LED_GPIO_Port, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc){
	// Toggle para visual
	// HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
	// Se agrega un dato al buffer
	// Pasa el valor del ADC de 12 bits a 8 bits
	uint8_t valorADC = (HAL_ADC_GetValue(&hadc1) & 0xFF0) >> 4;
	// El 0xFF es el código para indicar error asi que no puede ser usado
	if (valorADC == 0xFF)
		valorADC = 254;
	adc_buffer[adc_index] = valorADC;
	// Se incrementa el adc_index
	adc_index++;
	if (adc_index >= BUFFER_SIZE){
		adc_index = 0;
		error_buffer = 1;
	}
}


void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart){
	HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
	// Vuelve a esperar para recibir dato
	HAL_UART_Receive_IT(&huart2, &rx_dato, 1);
	// Resetea los contenidos del buffer
	for (uint16_t i=0; i<BUFFER_SIZE; i++){
		adc_buffer[i] = 0;
	}
	// Sale del modo enviar
	flag_cambio = 1;
	flag_actual = 0;
}


void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){
	flag_cambio = 1;
	flag_actual = rx_dato;
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
	while(1){
		HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
		HAL_Delay(200);
	}
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
