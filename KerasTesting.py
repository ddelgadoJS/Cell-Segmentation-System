# MLP for Pima Indians Dataset Serialize to JSON and HDF5
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.engine.saving import load_model

#model = Sequential()
model = Sequential([
    Dense(32, input_shape=(784,)),
    Activation('relu'),
    Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax'),Dense(10),
    Activation('softmax')
])

# load weights into model
model.load_weights("best_female_model.h5")

print("Loaded model from disk")

"""

model.add(Dense(12, input_dim=8, kernel_initializer='uniform', activation='relu'))
model.add(Dense(8, kernel_initializer='uniform', activation='relu'))
model.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, Y, epochs=150, batch_size=10, verbose=0)
# evaluate the model
scores = model.evaluate(X, Y, verbose=0)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
 
# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")


"""