




def dataset_custom_map_v1(dataset_name):
    """Converts a Hugging Face dataset to a Parquet file.
    Args:
        dataset_name (str):  name of  dataset.
        mapping (dict):  mapping of  column names. Defaults to None.
    """
    dataset = datasets.load_dataset(dataset_name)

    df
    # print(dataset)
    for key in dataset:
        df = pd.DataFrame(dataset[key])
        if mapping is not None:
            df = df.rename(columns=mapping)
        # print(df.head)



ksize=1000
kmax = int(len(df) // ksize) +1
for k in range(0, kmax):
    log(k)
    dirouk = f"{dirout}/{df}_{k}.parquet"
    pd_to_file( df.iloc[k*ksize:(k+1)*ksize, : ], dirouk, show=0)




## Recommended Imports
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    NamedSparseVector,
    NamedVector,
    SparseVector,
    PointStruct,
    SearchRequest,
    SparseIndexParams,
    SparseVectorParams,
    VectorParams,
    ScoredPoint,
)

## Creating a collection
client.create_collection(
    collection_name,
    vectors_config={
        "text-dense": VectorParams(
            size=1024,  # OpenAI Embeddings
            distance=Distance.COSINE,
        )
    },
    sparse_vectors_config={
        "text-sparse": SparseVectorParams(
            index=SparseIndexParams(
                on_disk=False,
            )
        )
    },
)

## Creating Points
points = []
for idx, (text, sparse_vector, dense_vector) in enumerate(
    zip(product_texts, sparse_vectors, dense_vectors)
):
    sparse_vector = SparseVector(
        indices=sparse_vector.indices.tolist(), values=sparse_vector.values.tolist()
    )
    point = PointStruct(
        id=idx,
        payload={
            "text": text,
            "product_id": rows[idx]["product_id"],
        },  # Add any additional payload if necessary
        vector={
            "text-sparse": sparse_vector,
            "text-dense": dense_vector,
        },
    )
    points.append(point)

## Upsert
client.upsert(collection_name, points)












