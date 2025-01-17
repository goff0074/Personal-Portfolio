dailykos <- read.table("dailykos.csv", sep = ",", header = TRUE)

kos_distances <- dist(dailykos, method = "euclidean")
kos_dist_matrix <- as.matrix(kos_distances)
rm(kos_dist_matrix)

cluster_kos <- hclust(kos_distances, method = "ward.D2")
plot(cluster_kos)

clusterGroups = cutree(cluster_kos, k = 8)

cluster1 <- subset(dailykos, clusterGroups == 1)
cluster2 <- subset(dailykos, clusterGroups == 2)
cluster3 <- subset(dailykos, clusterGroups == 3)
cluster4 <- subset(dailykos, clusterGroups == 4)
cluster5 <- subset(dailykos, clusterGroups == 5)
cluster6 <- subset(dailykos, clusterGroups == 6)
cluster7 <- subset(dailykos, clusterGroups == 7)
cluster8 <- subset(dailykos, clusterGroups == 8)

mean_cluster1 <- colMeans(cluster1)
top_words_1 <- sort(mean_cluster1, decreasing = TRUE)
top_5_1 <- head(top_words_1, 5)  
  
mean_cluster2 <- colMeans(cluster2)
top_words_2 <- sort(mean_cluster2, decreasing = TRUE)
top_5_2 <- head(top_words_2, 5)  
  
mean_cluster3 <- colMeans(cluster3)
top_words_3 <- sort(mean_cluster3, decreasing = TRUE)
top_5_3 <- head(top_words_3, 5)  
  
mean_cluster4 <- colMeans(cluster4)
top_words_4 <- sort(mean_cluster4, decreasing = TRUE)
top_5_4 <- head(top_words_4, 5)

mean_cluster5 <- colMeans(cluster5)
top_words_5 <- sort(mean_cluster5, decreasing = TRUE)
top_5_5 <- head(top_words_5, 5)  

mean_cluster6 <- colMeans(cluster6)
top_words_6 <- sort(mean_cluster6, decreasing = TRUE)
top_5_6 <- head(top_words_6, 5)  

mean_cluster7 <- colMeans(cluster7)
top_words_7 <- sort(mean_cluster7, decreasing = TRUE)
top_5_7 <- head(top_words_7, 5)  

mean_cluster8 <- colMeans(cluster8)
top_words_8 <- sort(mean_cluster8, decreasing = TRUE)
top_5_8 <- head(top_words_8, 5)  

print(top_5_1)
print(top_5_2)
print(top_5_3)
print(top_5_4)
print(top_5_5)
print(top_5_6)
print(top_5_7)
print(top_5_8)


data("USArrests")
arrests_distances <- dist(USArrests, method = "euclidean")
cluster_arrest <- hclust(arrests_distances, method = "complete")
plot(cluster_arrest)

arrest_dend_clusters <- cutree(cluster_arrest, k = 3)

state_cluster1 <- subset(USArrests, arrest_dend_clusters == 1)
state_names_cluster1 <- rownames(state_cluster1)
print(state_names_cluster1)

state_cluster2 <- subset(USArrests, arrest_dend_clusters == 2)
state_names_cluster2 <- rownames(state_cluster2)
print(state_names_cluster2)

state_cluster3 <- subset(USArrests, arrest_dend_clusters == 3)
state_names_cluster3 <- rownames(state_cluster3)
print(state_names_cluster3)

cluster_arrest_ward <- hclust(arrests_distances, method = "ward.D2")
plot(cluster_arrest_ward)

arrest_dend_clusters_ward <- cutree(cluster_arrest_ward, k = 3)

state_cluster1_ward <- subset(USArrests, arrest_dend_clusters_ward == 1)
state_names_cluster1_ward <- rownames(state_cluster1_ward)
print(state_names_cluster1_ward)

state_cluster2_ward <- subset(USArrests, arrest_dend_clusters_ward == 2)
state_names_cluster2_ward <- rownames(state_cluster2_ward)
print(state_names_cluster2_ward)

state_cluster3_ward <- subset(USArrests, arrest_dend_clusters_ward == 3)
state_names_cluster3_ward <- rownames(state_cluster3_ward)
print(state_names_cluster3_ward)

arrests_scaled <- scale(USArrests)
arrests_dist_scaled <- dist(arrests_scaled, method = "euclidean")
hclust_model_scaled <- hclust(arrests_dist_scaled, method = "complete")
plot(hclust_model_scaled)

clust_scaled <- cutree(hclust_model_scaled, k = 5)
table(clust_scaled)



