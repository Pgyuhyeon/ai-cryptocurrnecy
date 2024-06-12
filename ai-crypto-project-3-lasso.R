## https://github.com/Pgyuhyeon 박규현, 김우리

library('stringr')
library('glmnet')

# 회귀 계수를 추출하는 함수
extract <- function(o, s) { 
  index <- which(coef(o, s) != 0) 
  data.frame(name=rownames(coef(o))[index], coef=coef(o, s)[index]) 
}

options(scipen=999)

args <- commandArgs(TRUE)

# 인수: 시작 시간, 종료 시간, 거래소, 코인 심볼, mid5
start_time <- args[1]
end_time <- args[2]
exchange <- args[3]
coin_symbol <- args[4]
mid5 <- args[5]

filtered <- paste(start_time, end_time, exchange, coin_symbol, 'filtered-5-2', mid5, sep="-")
model_file <- paste(end_time, exchange, coin_symbol, mid5, 'lasso-5s-2std', sep='-')

# 파일 이름에서 콜론 제거
filtered <- str_remove_all(filtered, ":")
model_file <- str_remove_all(model_file, ":")

filtered <- paste("./", filtered, ".csv", sep="")
model_file <- paste("./", model_file, ".csv", sep="")

# 데이터 읽기
filtered <- read.csv(filtered)

# 중간 가격의 표준편차 계산
mid_std <- sd(filtered$mid_price)
message(round(mid_std, 0))

# 시간과 중간 가격 열 제거
filtered_no_time_mid <- subset(filtered, select = -c(mid_price, timestamp))

# 종속 변수와 독립 변수 분리
y <- filtered_no_time_mid$return
x <- subset(filtered_no_time_mid, select = -c(return))

# 매트릭스 형식으로 변환
x <- as.matrix(x)

# Lasso 회귀 모델 학습
cv_fit <- cv.glmnet(x = x, y = y, alpha = 1, intercept = FALSE, lower.limits = 0, nfolds = 5)

fit <- glmnet(x = x, y = y, alpha = 1, lambda = cv_fit$lambda.1se, intercept = FALSE, lower.limits = 0)

# 회귀 계수 추출
df <- extract(fit, s = 0.1)
df <- t(df)

# 결과 파일로 저장
write.table(df, file = model_file, sep = ",", col.names = FALSE, row.names = FALSE, quote = FALSE)

##이 코드는 주어진 인수(시작 시간, 종료 시간, 거래소, 코인 심볼, mid5)를 기반으로 파일 이름을 생성하고, 
#필터링된 데이터를 읽어와 Lasso 회귀 모델을 학습합니다. 데이터에서 시간과 중간 가격 열을 제거한 후, 
#종속 변수와 독립 변수를 분리하여 매트릭스 형식으로 변환합니다. 
#cv.glmnet 함수를 사용해 교차 검증을 통해 최적의 람다 값을 찾고, 
#glmnet 함수를 사용해 Lasso 회귀 모델을 학습합니다. 
#마지막으로, 회귀 계수를 추출하여 결과를 CSV 파일로 저장합니다.