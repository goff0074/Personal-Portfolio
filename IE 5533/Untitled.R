dailykos <- read.table("dailykos.csv", sep = ",", header = TRUE)
set.seed(55332024)
str(dailykos)

k <- 7
kos_kmeans <- kmeans(dailykos, centers = k, nstart = 10)
print(kos_kmeans)

cluster_centers <- kos_kmeans$centers
print(cluster_centers[, 1:7])

kmeans_clusters <- kos_kmeans$cluster

top_words_list <- list()

for (i in 1:7) {
  # Subset the data for the current cluster
  cluster_data <- dailykos[kmeans_clusters == i, ]
  
  # Calculate column means
  mean_cluster <- colMeans(cluster_data)
  mean_cluster <- mean_cluster[names(mean_cluster) != "cluster"]
  
  # Sort and get top 5 words
  top_words <- sort(mean_cluster, decreasing = TRUE)
  top_5_words <- head(top_words, 5)
  
  # Store the result in the list
  top_words_list[[i]] <- top_5_words
}

# Print top 5 words for each cluster
for (i in 1:7) {
  cat(paste("Top 5 words for Cluster", i, ":\n"))
  print(top_words_list[[i]])
  cat("\n")
}

kos_distances <- dist(dailykos, method = "euclidean")
cluster_kos <- hclust(kos_distances, method = "ward.D2")

h_clust <- cutree(cluster_kos, k)
confusion_matrix <- table(KMeans = kmeans_clusters, Hierarchical = h_clust)
print(confusion_matrix)

#QUESTION 2)
library(ggplot2)
points_data <- read.csv("points_data.csv")

metrics <- data.frame(k = integer(), within_cluster_sums = numeric())
for (k in 1:10) {
  points_kmc <- kmeans(points_data, centers = k, nstart = 10)
  metrics <- rbind(metrics, data.frame(k = k, within_cluster_sums = points_kmc$tot.withinss))
}
print(metrics)

ggplot(data = metrics, aes(x = k, y = within_cluster_sums)) +
  geom_point(size = 4, shape = 20, col = "blue") +
  geom_line() +
  ggtitle("Scree Plot") +
  theme_bw() +
  theme(text = element_text(size = 25))

points_kmc <- kmeans(points_data, centers = 3, nstart = 10)
print(points_kmc$centers)

points_data$cluster <- as.factor(points_kmc$cluster)

ggplot(points_data, aes(x = x, y = y, color = cluster)) +  
  geom_point(size = 3) +
  ggtitle(paste("K-means Clustering with k =", 3)) +
  theme_bw() +
  theme(text = element_text(size = 25)) +
  scale_color_discrete(name = "Clusters") +
  labs(x = "X Coordinate", y = "Y Coordinate")


library(flexclust)
points_test_data <- read.csv("points_test_data.csv")
points_kmc <- kmeans(points_data[, c("x", "y")], centers = 3, nstart = 10)

points_kcca <- as.kcca(points_kmc, points_data[, c("x", "y")])
predicted_clusters <- predict(points_kcca, newdata = points_test_data[, c("x", "y")])
print(predicted_clusters)

predictions_df <- data.frame(points_test_data, predicted_cluster = predicted_clusters)
print(predictions_df)

confusion_matrix <- table(predicted = predictions_df$predicted_cluster, actual = predictions_df$source)
print(confusion_matrix)
