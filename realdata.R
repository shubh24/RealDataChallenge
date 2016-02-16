# Enter your code here. Read input from STDIN. Print output to STDOUT
args <- commandArgs(trailingOnly=TRUE)

#f <- file("stdin")
#open(f)
#data <- c()
#while(length(line <- readLines(f,n=1, warn = FALSE)) > 0) {
#  data <- c(data, line)
#}

f = read.csv('realcsv.csv')

n = args[1]
n = as.numeric(n)
data = c()
#for(i in 2:n+1){
#	 data = c(data,args[i])
#}

for(i in 1:n+1){
	 data = c(data,f$X500[i])
}

df <- data.frame(sessions = numeric(n), stringsAsFactors = FALSE)
	
for (i in 1:n){
	df$sessions[i] = data[i]
}	

df$sessions = as.numeric(df$sessions)

library(stats)
x11()
plot(df$sessions,type="l",xlim=c(0,500))
Sys.sleep(4)

df2 = as.matrix(df$sessions)


model = arima(df2,order=c(2,1,5),seasonal=list(order = c(2,1,2), period = 60),method="CSS")
forecast = (predict(model,30))

f2 = as.data.frame(forecast)
new = c(data,f2$pred)
plot(new,type="l")
Sys.sleep(10)



for(i in 1:30){
    write(as.integer(f2$pred[i]),stdout())
}
