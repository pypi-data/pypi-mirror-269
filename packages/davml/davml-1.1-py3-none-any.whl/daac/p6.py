# Create data frame of students' information
students <- data.frame(
  Name = c("John", "Emily", "Michael", "Sophia", "Daniel", "Olivia", "William", "Ava", "James", "Isabella"),
  Subject = rep(c("Math", "Science", "English"), each = 10),
  Marks = sample(60:100, 30, replace = TRUE)  # Generating random marks for demonstration
)


# Plot boxplot for subjects
boxplot(Marks ~ Subject, data = students)
# View the data frame
View(students)

# Read the CSV file into a data frame
startup_data <- read.csv("startup_funding.csv")

# Display the top 5 rows of the data frame in table format
print(head(startup_data, n = 5))
# Load required libraries
library(ggplot2)

# Create a subset of data with top 5 categories
top_5_categories <- c("E-Tech", "Transportation", "E-commerce", "FinTech", "Fashion and Apparel")
subset_data <- subset(startup_data, Industry.Vertical %in% top_5_categories)

# Create a bar plot
ggplot(subset_data, aes(x = Industry.Vertical)) +
  geom_bar(fill = "skyblue", color = "black") +
  labs(title = "Count of Startups by Industry (Top 5 Categories)",
       x = "Industry",
       y = "Count") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Load required libraries
library(ggplot2)

# Create a subset of data with top 5 categories
top_5_categories <- c("E-Tech", "Transportation", "E-commerce", "FinTech", "Fashion and Apparel")
subset_data <- subset(startup_data, Industry.Vertical %in% top_5_categories)

# Calculate frequency of startups in each category
category_counts <- table(subset_data$Industry.Vertical)

# Create a pie chart
pie(category_counts, labels = names(category_counts), col = rainbow(length(category_counts)),
    main = "Distribution of Startups by Industry (Top 5 Categories)")

# Load required libraries
library(ggplot2)

# Create a subset of data with top 5 categories
top_5_categories <- c("E-Tech", "Transportation", "E-commerce", "FinTech", "Fashion and Apparel")
subset_data <- subset(startup_data, Industry.Vertical %in% top_5_categories)

# Create a box plot
ggplot(subset_data, aes(x = Industry.Vertical, y = as.numeric(gsub(",", "", Amount.in.USD)))) +
  geom_boxplot(fill = "skyblue", color = "black") +
  labs(title = "Distribution of Startups by Industry (Top 5 Categories)",
       x = "Industry",
       y = "Amount in USD") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Load required libraries
library(ggplot2)

# Select the top 10 data points
top_10_data <- head(startup_data, 10)

# Create a histogram for funding amounts across industries
ggplot(top_10_data, aes(x = as.numeric(gsub(",", "", Amount.in.USD)))) +
  geom_histogram(binwidth = 1000000, fill = "skyblue", color = "black") +
  labs(title = "Histogram of Funding Amounts (Top 10 Data)",
       x = "Funding Amount (USD)",
       y = "Frequency") +
  theme_minimal()

# Load required libraries
library(ggplot2)

# Select the top 10 data points
top_10_data <- head(startup_data, 10)

# Create a scatter plot for location and industry
ggplot(top_10_data, aes(x = City..Location, y = Industry.Vertical)) +
  geom_point(color = "skyblue") +
  labs(title = "Top 10 Startups: Location vs Industry",
       x = "Location",
       y = "Industry") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Rotate x-axis labels for better readability


# Load required libraries
library(ggplot2)
library(dplyr)

# Select the top 10 data points
top_10_data <- head(startup_data, 10)

# Create a dataframe for heatmap
heatmap_data <- top_10_data %>%
  group_by(City..Location, Industry.Vertical) %>%
  summarise(count = n())

# Create a heatmap for location and industry
ggplot(heatmap_data, aes(x = City..Location, y = Industry.Vertical, fill = count)) +
  geom_tile() +
  labs(title = "Heatmap of Top 10 Startups: Location vs Industry",
       x = "Location",
       y = "Industry",
       fill = "Count") +
  scale_fill_gradient(low = "lightblue", high = "darkblue") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Rotate x-axis labels for better readability
